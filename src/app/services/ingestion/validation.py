from __future__ import annotations

from app.services.ingestion.types import (
    CanonicalIngestionRecord,
    QualityFlag,
    ValidationStatus,
)


def validate_record(record: CanonicalIngestionRecord) -> CanonicalIngestionRecord:
    quality_flags = list(record.quality_flags)

    if not record.title.strip():
        record.validation_status = ValidationStatus.REJECTED
        return record

    if not record.body_text.strip():
        record.validation_status = ValidationStatus.REJECTED
        return record

    if record.published_at is None:
        if QualityFlag.PARTIAL_PARSE not in quality_flags:
            quality_flags.append(QualityFlag.PARTIAL_PARSE)
        record.quality_flags = quality_flags
        record.validation_status = ValidationStatus.QUARANTINED
        return record

    if quality_flags:
        record.quality_flags = quality_flags
        record.validation_status = ValidationStatus.ACCEPTED_WITH_FLAGS
        return record

    record.validation_status = ValidationStatus.ACCEPTED
    return record
