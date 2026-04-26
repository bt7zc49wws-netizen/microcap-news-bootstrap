from app.models.ingestion_record import IngestionRecord


def classify_record(record: IngestionRecord) -> dict:
    headline_lower = record.headline.lower()

    financing_keywords = (
        "financing",
        "offering",
        "convertible note",
        "exercise of warrants",
        "gross proceeds",
    )

    if any(keyword in headline_lower for keyword in financing_keywords):
        return {
            "event_family": "financing",
            "event_type": "financing_news",
            "classification_status": "EVENT_CANDIDATE",
            "reason_code": "FINANCING_KEYWORD_MATCH",
            "reason_label": "Financing keyword match",
            "candidate_priority": "high",
            "decision_hint": "watchlist_candidate",
            "explanation_summary": "Headline matched financing-related event language.",
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
        "decision_hint": "ignore_candidate",
        "explanation_summary": "No clear event keyword match was detected.",
        "source_quality_flags": record.quality_flags,
        "noise_flags": '["low_signal"]',
    }
