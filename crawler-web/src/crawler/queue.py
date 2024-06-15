import queue

class UrlQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.processed_urls = set()
    
    def put(self, url: str):
        formatted_url: str = url.rstrip("/")

        if formatted_url in self.processed_urls:
            return
        self.processed_urls.add(formatted_url)
        self.queue.put(formatted_url)
    
    def get(self, timeout: int) -> str:
        return self.queue.get(timeout=timeout)
    
    def empty(self) -> bool:
        return self.queue.empty()
    