from app.models.ingestion_record import IngestionRecord


def classify_record(record: IngestionRecord) -> dict:
    headline_lower = record.headline.lower()

    if "financing" in headline_lower:
        return {
            "event_family": "financing",
            "event_type": "financing_news",
            "classification_status": "EVENT_CANDIDATE",
            "reason_code": "FINANCING_KEYWORD_MATCH",
            "reason_label": "Financing keyword match",
            "candidate_priority": "high",
            "source_quality_flags": record.quality_flags,
            "noise_flags": "[]",
        }

    if "offering" in headline_lower:
        return {
            "event_family": "financing",
            "event_type": "offering_news",
            "classification_status": "EVENT_CANDIDATE",
            "reason_code": "OFFERING_KEYWORD_MATCH",
            "reason_label": "Offering keyword match",
            "candidate_priority": "high",
            "source_quality_flags": record.quality_flags,
            "noise_flags": "[]",
        }

    return {
        "event_family": "other",
        "event_type": "uncategorized",
        "classification_status": "LOW_PRIORITY_CANDIDATE",
        "reason_code": "NO_CLEAR_EVENT_MATCH",
        "reason_label": "No clear event match",
        "candidate_priority": "low",
        "source_quality_flags": record.quality_flags,
        "noise_flags": '["low_signal"]',
    }
