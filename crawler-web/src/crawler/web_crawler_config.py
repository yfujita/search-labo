from dataclasses import dataclass, field

@dataclass
class WebCrawlerConfig:
    max_depth: int
    max_pages: int
    timeout_sec: int = 60
    interval_sec: int = 1
    ignore_url_patterns: list[str] = field(default_factory=list)