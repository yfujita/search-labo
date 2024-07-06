from dataclasses import dataclass, field

@dataclass
class WebCrawlerConfig:
    max_pages: int
    max_depth: int = -1
    timeout_sec: int = 60
    interval_sec: int = 1
    crawl_include_url_patterns: list[str] = field(default_factory=list)
    crawl_exclude_url_patterns: list[str] = field(default_factory=list)
    data_include_url_patterns: list[str] = field(default_factory=list)
    data_exclude_url_patterns: list[str] = field(default_factory=list)
    crawl_interval_mills: int = 1000