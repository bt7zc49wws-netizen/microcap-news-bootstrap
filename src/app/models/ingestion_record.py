
class IngestionRecord:
    def __init__(self, **kwargs):
        self.headline = kwargs.get("headline", "")
        self.symbol = kwargs.get("symbol", "")
        self.quality_flags = kwargs.get("quality_flags", [])

def validate_ingestion_record(record):
    if not hasattr(record, "headline"):
        raise ValueError("missing_headline")
    return True
