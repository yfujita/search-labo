import requests
import time
import urllib
import urllib.robotparser
import re
import traceback

from extractor.protocol import ExtractorProtocol
from exporter.protocol import ExporterProtocol
from exporter.export_content import ExportContent
from .web_crawler_config import WebCrawlerConfig
from .queue import UrlQueue

class WebCrawler:
    USER_AGENT='SearchLaboCrawler/1.0'

    def __init__(
        self,
        extractor: ExtractorProtocol,
        exporter: ExporterProtocol,
        url_queue: UrlQueue,
        config: WebCrawlerConfig,
        ):
        self.url_queue = url_queue
        self.config = config
        self.extractor = extractor
        self.exporter = exporter
        self.processed_count = 0
    
    def run(self):
        while True:
            url: str
            try:
                print('Poll next URL.', flush=True)
                url = self.url_queue.get(timeout=self.config.timeout_sec)
            except queue.Empty:
                print('URL queue is empty. Finish crawling.', flush=True)
                break
            
            print(f'Crawling url: {url}', flush=True)
            
            try:
                if not self._can_fetch(url):
                    print(f'URL {url} is not allowed to crawl.', flush=True)
                    continue

                self._crawl(url)
                self.processed_count += 1
                if self.config.max_pages <= self.processed_count:
                    print(f'Max pages ({self.processed_count}) reached. Finish crawling.', flush=True)
                    break
            except Exception as e:
                print(f'Error crawling {url}: {e}', flush=True)
                traceback.print_exc()
            
            time.sleep(self.config.interval_sec)
    
    def _crawl(self, url: str):
        data = self._fetch(url)
        extract_result = self.extractor.extract(url, data)
        
        for link in extract_result.links:
            ignore: bool = False
            for ignore_url_pattern in self.config.ignore_url_patterns:
                if re.match(ignore_url_pattern, link):
                    ignore = True
                    break
            if not ignore:
                self.url_queue.put(link)
        
        if not extract_result.title:
            print(f'No title found for {url}', flush=True)
            return

        export_content = ExportContent(
            url=url,
            title=extract_result.title,
            content=extract_result.content,
            attrs={'images': extract_result.image_links, 'thumbnail': extract_result.thumbnail_link},
        )
        self.exporter.export(export_content)        
    
    def _fetch(self, url: str) -> bytes:
        response = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        return response.content
    
    def _can_fetch(self, url) -> bool:
        parsed_url = urllib.parse.urlparse(url)
        robots_url = f'{parsed_url.scheme}://{parsed_url.netloc}/robots.txt'
        
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        return rp.can_fetch(self.USER_AGENT, url)
