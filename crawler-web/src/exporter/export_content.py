from dataclasses import dataclass

@dataclass
class ExportContent:
    url: str
    title: str
    content: str
    attrs: dict
