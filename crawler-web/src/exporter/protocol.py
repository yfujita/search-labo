from typing import Protocol
from .export_content import ExportContent

class ExporterProtocol(Protocol):
    def export(self, content: ExportContent) -> None:
        pass
    
    def get_count(self) -> int:
        pass