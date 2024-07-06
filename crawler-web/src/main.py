import os
import threading
import json
from pathlib import Path

from crawler.web_crawler_config import WebCrawlerConfig
from crawler.web_crawler import WebCrawler
from crawler.queue import UrlQueue
from extractor.web_extractor import WebExtractor
from extractor.protocol import ExtractorProtocol
from extractor.extract_result import ExtractResult
from exporter.ndjson_exporter import NdjsonExporter
from exporter.protocol import ExporterProtocol

def main():
    env = os.environ.get('ENV')
    if env is None or env == '':
        print('ENV is not set.', flush=True)
        exit(1)
    print(f'ENV: {env}', flush=True)

    config = load_config(env)
    crawl_target_urls: list[str] = config['crawl_target_urls']
    crawl_include_url_patterns: list[str] = config['crawl_include_url_patterns']
    crawl_exclude_url_patterns: list[str] = config['crawl_exclude_url_patterns']
    data_include_url_patterns: list[str] = config['data_include_url_patterns']
    data_exclude_url_patterns: list[str] = config['data_exclude_url_patterns']
    max_pages: int = config['max_pages']
    thread_num: int = config['thread_num']
    crawl_interval_mills: int = config['crawl_interval_mills']

    extractor = WebExtractor()
    exporter = NdjsonExporter(output_dir='/output', output_file_prefix='content', seperate_content_size=100)

    # Add target urls to queue
    url_queue = UrlQueue()
    for url in crawl_target_urls:
        url_queue.put(url)

    config = WebCrawlerConfig(
        max_pages=max_pages,
        timeout_sec=10,
        crawl_include_url_patterns=crawl_include_url_patterns,
        crawl_exclude_url_patterns=crawl_exclude_url_patterns,
        data_include_url_patterns=data_include_url_patterns,
        data_exclude_url_patterns=data_exclude_url_patterns,
        crawl_interval_mills=crawl_interval_mills,
    )

    threads = []
    for _ in range(thread_num):
        thread = threading.Thread(target=run_crawler, args=(extractor, exporter, url_queue, config))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print('All threads are finished.')

def load_config(env: str) -> dict:
    config_path = Path(__file__).parent / 'config' / f'{env}.json'
    if not config_path.exists():
        print(f'Config file not found: {config_path}', flush=True)
        exit(1)

    with open(config_path) as f:
        config = json.load(f)
        return config

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