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
        self.robots_cache = {}
    
    def run(self):
        while True:
            if self.exporter.get_count() >= self.config.max_pages:
                print(f'Max pages ({self.config.max_pages}) reached. Finish crawling.', flush=True)
                break

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
            except Exception as e:
                print(f'Error crawling {url}: {e}', flush=True)
                traceback.print_exc()
            
            time.sleep(self.config.crawl_interval_mills / 1000)
    
    def _crawl(self, url: str):
        data = self._fetch(url)
        extract_result = self.extractor.extract(url, data)
        
        # Extract links and put them to queue
        for link in extract_result.links:
            ignore: bool = False
            
            if len(self.config.crawl_include_url_patterns) > 0:
                ignore = True
                for crawl_include_url_pattern in self.config.crawl_include_url_patterns:
                    if re.match(crawl_include_url_pattern, link):
                        ignore = False
                        break
            
            for crawl_exclude_url_pattern in self.config.crawl_exclude_url_patterns:
                if re.match(crawl_exclude_url_pattern, link):
                    ignore = True
                    break
            if not ignore:
                self.url_queue.put(link)
        
        if not extract_result.title:
            print(f'No title found for {url}', flush=True)
            return

        # Export data
        ignore_data: bool = False
        if len(self.config.data_include_url_patterns) > 0:
                ignore_data = True
                for data_include_url_pattern in self.config.data_include_url_patterns:
                    if re.match(data_include_url_pattern, url):
                        ignore_data = False
                        break
            
        for data_exclude_url_pattern in self.config.data_exclude_url_patterns:
            if re.match(data_exclude_url_pattern, url):
                ignore_data = True
                break
        
        if not ignore_data:
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
        
        if parsed_url.netloc in self.robots_cache:
            return self.robots_cache[parsed_url.netloc]

        robots_url = f'{parsed_url.scheme}://{parsed_url.netloc}/robots.txt'
        
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        can_fetch: bool = rp.can_fetch(self.USER_AGENT, url)
        self.robots_cache[parsed_url.netloc] = can_fetch
        return can_fetch
