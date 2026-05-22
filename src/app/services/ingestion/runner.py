from dataclasses import dataclass
from xml.etree import ElementTree

from app.db import SessionLocal
from app.models.ingestion_record_db import IngestionRecordDB


@dataclass
class IngestionRun:
    run_status: str
    records_fetched: int


@dataclass
class CanonicalIngestionRecord:
    source_record_id: str


def persist_ingestion_records(records):
    session = SessionLocal()

    try:
        for record in records:
            external_id = getattr(record, "source_record_id", None)

            if external_id is None:
                continue

            exists = (
                session.query(IngestionRecordDB)
                .filter_by(external_id=external_id)
                .first()
            )

            if exists is not None:
                continue

        session.commit()

    except Exception:
        session.rollback()

    finally:
        session.close()


def run_live_ingestion(
    config,
    http_client=None,
    persist=True,
):
    if not config.live_source_enabled:
        raise ValueError("Live source ingestion is disabled.")

    if not config.live_source_url.strip():
        raise ValueError(
            "LIVE_SOURCE_URL must be set when live ingestion is enabled."
        )

    if http_client is None:
        raise ValueError("http_client_required")

    response = http_client.get(
        config.live_source_url,
        timeout=config.live_source_timeout_seconds,
    )

    response.raise_for_status()

    raw_records = [response.text]

    root = ElementTree.fromstring(response.text)

    canonical_records = []

    for item in root.findall(".//item"):
        guid = item.findtext("guid")

        if guid:
            canonical_records.append(
                CanonicalIngestionRecord(
                    source_record_id=guid,
                )
            )

    canonical_records = canonical_records[
        : config.live_source_max_items_per_run
    ]

    if persist:
        persist_ingestion_records(canonical_records)

    run = IngestionRun(
        run_status="completed",
        records_fetched=len(canonical_records),
    )

    return (
        run,
        raw_records,
        canonical_records,
    )
