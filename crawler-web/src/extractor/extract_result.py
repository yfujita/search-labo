from dataclasses import dataclass

@dataclass
class ExtractResult:
    title: str
    content: str
    image_links: list[str]
    links: list[str]
    thumbnail_link: str