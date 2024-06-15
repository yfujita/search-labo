from .extract_result import ExtractResult

class SampleExtractor:
    def extract(self, url: str, data: bytes) -> ExtractResult:
        return ExtractResult(
            title="Example",
            content="This is an example.",
            image_links=[],
            links=["https://example.com"],
            thumbnail_link='',
        )