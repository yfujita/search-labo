from typing import Protocol
from .extract_result import ExtractResult

class ExtractorProtocol(Protocol):
    def extract(self, url: str, data: bytes) -> ExtractResult:
        pass