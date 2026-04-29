from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ProviderFetchResult:
    provider_name: str
    fetched_at: datetime
    records_returned: int
    status: str
    error_message: str | None = None
    payload: dict | list | None = None

    def to_status_diagnostic(self) -> dict:
        diagnostic = {
            "provider_name": self.provider_name,
            "status": self.status,
            "records_returned": self.records_returned,
            "fetched_at": self.fetched_at.isoformat(),
            "has_error": self.error_message is not None,
        }
        if self.error_message is not None:
            diagnostic["error_message"] = self.error_message
        return diagnostic
