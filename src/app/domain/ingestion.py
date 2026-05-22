
from dataclasses import dataclass

@dataclass
class IngestionRecord:
    record_id: str
    source_name: str = ""
