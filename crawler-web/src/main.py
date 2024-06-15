import threading

from crawler.web_crawler_config import WebCrawlerConfig
from crawler.web_crawler import WebCrawler
from crawler.queue import UrlQueue
from extractor.web_extractor import WebExtractor
from extractor.protocol import ExtractorProtocol
from extractor.extract_result import ExtractResult
from exporter.ndjson_exporter import NdjsonExporter
from exporter.protocol import ExporterProtocol

def main():
    extractor = WebExtractor()
    exporter = NdjsonExporter(output_dir='/output', output_file_prefix='content', seperate_content_size=100)

    url_queue = UrlQueue()
    url_queue.put('https://b.hatena.ne.jp/')
    url_queue.put('https://news.yahoo.co.jp/topics/top-picks')

    config = WebCrawlerConfig(
        max_depth=1,
        max_pages=10000,
        timeout_sec=10,
        ignore_url_patterns=[
            '.*hatenabookmark.*',
            '.*://.*/.*/.*/.*',
            '.*/q/.*',
            'https://www.yahoo.co.jp/.*',
            '.*\\?.*',
            '.*/keyword/.*',
        ]
    )

    threads = []
    for _ in range(3):
        thread = threading.Thread(target=run_crawler, args=(extractor, exporter, url_queue, config))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print('All threads are finished.')

def run_crawler(extractor: ExtractorProtocol, exporter: ExporterProtocol, url_queue: UrlQueue, config: WebCrawlerConfig):
    crawler = WebCrawler(
        extractor=extractor,
        exporter=exporter,
        url_queue=url_queue,
        config=config,
    )
    crawler.run()

if __name__ == '__main__':
    main()