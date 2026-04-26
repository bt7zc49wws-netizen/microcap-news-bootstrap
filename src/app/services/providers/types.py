from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ProviderFetchResult:
    provider_name: str
    fetched_at: datetime
    records_returned: int
    status: str
    error_message: str | None = None
