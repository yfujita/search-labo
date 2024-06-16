from typing import Protocol
from .bulk_item import BulkItem

class DatabuildProtocol(Protocol):
    def build(self, index: str, content: str) -> BulkItem:
        pass