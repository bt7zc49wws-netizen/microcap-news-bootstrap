from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from hashlib import sha256
from typing import Any
from uuid import uuid4
import urllib.request
import re
import xml.etree.ElementTree as ET

from app.services.ingestion.types import (
    CanonicalIngestionRecord,
    QualityFlag,
    RawSourceRecord,
    ValidationStatus,
)


SOURCE_NAME = "press_release_feed_v1"
ADAPTER_VERSION = "press_release_feed_adapter_v1"
NORMALIZATION_VERSION = "canonical_ingest_v1"


@dataclass(slots=True)
class PressReleaseFeedItem:
    source_record_id: str
    title: str
    body_text: str
    source_url: str | None
    published_at: datetime | None
    primary_ticker: str | None = None
    company_name: str | None = None
    language: str | None = "en"


_TICKER_PATTERN = re.compile(r"\b(?:NASDAQ|NYSE|NYSE American|AMEX):\s*([A-Z]{1,5})\b| - ([A-Z]{1,5})$")


def extract_primary_ticker(title: str, body_text: str) -> str | None:
    title_match = re.search(r" - ([A-Z]{1,5})$", title)
    if title_match:
        return title_match.group(1)

    text = f"{title}\n{body_text}"
    match = _TICKER_PATTERN.search(text)
    return next((group for group in match.groups() if group), None) if match else None


def compute_content_hash(title: str, body_text: str) -> str:
    payload = f"{title.strip()}\n{body_text.strip()}".encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def build_raw_record(
    item: dict[str, Any],
    *,
    fetch_run_id: str,
    fetched_at: datetime,
) -> RawSourceRecord:
    source_record_id = str(item.get("guid") or item.get("id") or item.get("link") or uuid4())
    source_url = item.get("link")
    title = str(item.get("title") or "").strip()
    body_text = str(item.get("content") or item.get("description") or "").strip()
    content_hash = compute_content_hash(title=title, body_text=body_text)

    return RawSourceRecord(
        raw_record_id=str(uuid4()),
        source_name=SOURCE_NAME,
        source_record_id=source_record_id,
        fetch_run_id=fetch_run_id,
        fetched_at=fetched_at,
        source_url=source_url,
        raw_payload=item,
        content_hash=content_hash,
        adapter_version=ADAPTER_VERSION,
    )


def normalize_item(
    item: dict[str, Any],
    *,
    ingested_at: datetime | None = None,
) -> CanonicalIngestionRecord:
    ingested_at = ingested_at or datetime.now(timezone.utc)
    processed_at = ingested_at

    source_record_id = str(item.get("guid") or item.get("id") or item.get("link") or uuid4())
    source_url = item.get("link")
    title = str(item.get("title") or "").strip()
    body_text = str(item.get("content") or item.get("description") or "").strip()
    published_at = item.get("published_at")
    primary_ticker = item.get("primary_ticker") or extract_primary_ticker(title, body_text)
    company_name = item.get("company_name")
    language = item.get("language") or "en"

    quality_flags: list[QualityFlag] = []

    if not item.get("content") and item.get("description"):
        quality_flags.append(QualityFlag.BODY_FROM_DESCRIPTION)

    if not primary_ticker:
        quality_flags.append(QualityFlag.TICKER_MISSING)

    validation_status = (
        ValidationStatus.ACCEPTED_WITH_FLAGS
        if quality_flags
        else ValidationStatus.ACCEPTED
    )

    content_hash = compute_content_hash(title=title, body_text=body_text)
    dedupe_key = f"{SOURCE_NAME}:{source_record_id}"

    return CanonicalIngestionRecord(
        record_id=str(uuid4()),
        source_name=SOURCE_NAME,
        source_record_id=source_record_id,
        source_url=source_url,
        title=title,
        body_text=body_text,
        published_at=published_at,
        ingested_at=ingested_at,
        processed_at=processed_at,
        primary_ticker=primary_ticker,
        company_name=company_name,
        language=language,
        content_hash=content_hash,
        dedupe_key=dedupe_key,
        is_duplicate=False,
        is_stale=False,
        validation_status=validation_status,
        quality_flags=quality_flags,
        raw_record_ref=None,
        normalization_version=NORMALIZATION_VERSION,
    )


_RELEVANT_TITLE_KEYWORDS = (
    "financing",
    "offering",
    "registered direct",
    "at-the-market",
    "shelf",
    "convertible note",
    "warrant",
    "gross proceeds",
)


def is_relevant_feed_item(item: dict[str, Any]) -> bool:
    text = " ".join(
        str(item.get(field) or "")
        for field in ("title", "description", "content")
    ).lower()
    return any(keyword in text for keyword in _RELEVANT_TITLE_KEYWORDS)


def parse_published_at(value: str | None) -> datetime | None:
    if not value:
        return None

    text = value.strip()
    if not text:
        return None

    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    try:
        iso_text = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def extract_items(xml_text: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    items: list[dict[str, Any]] = []

    for node in root.findall(".//item"):
        guid = node.findtext("guid")
        title = node.findtext("title")
        link = node.findtext("link")
        pub_date = node.findtext("pubDate") or node.findtext("published") or node.findtext("updated")
        description = node.findtext("description")
        content = node.findtext("content")

        item = {
            "guid": guid.strip() if guid else None,
            "title": title.strip() if title else "",
            "link": link.strip() if link else None,
            "description": description.strip() if description else "",
            "content": content.strip() if content else "",
            "published_at": parse_published_at(pub_date),
        }
        if is_relevant_feed_item(item):
            items.append(item)

    return items


def fetch_feed(
    url: str,
    *,
    http_client: Any | None = None,
    timeout: int = 15,
) -> str:
    if http_client is not None:
        response = http_client.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "microcap-news-bootstrap/0.1 (+https://example.invalid)",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")
