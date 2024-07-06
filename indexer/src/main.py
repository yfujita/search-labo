import os
import sys
import time
import json

from client.es_client import EsClient
from databuild.factory import DataBuilderFactory
from databuild.protocol import DatabuildProtocol
from databuild.bulk_item import BulkItem

def main():
    env: str = os.getenv('ENV')
    if env is None or env == '':
        print('ENV is not set.', flush=True)
        exit(1)
    
    print(f'Starting Indexer. ENV={env}', flush=True)

    es_client = EsClient(
        es_url = 'http://es:9200'
    )

    databuild_factory = DataBuilderFactory()

    # ES起動完了待ち
    for i in range(60):
        print('Wait for startup.', flush=True)
        if es_client.ping():
            break
        time.sleep(1)

    # 対象インデックス
    indices: list[str] = ['search-basic', 'search-knn']

    # インデックスセットアップ
    for index in indices:
        # 存在チェック
        if es_client.existIndex(index):
            print(f'Index {index} already exists. Skip setup process.', flush=True)
            continue
        
        # 設定ファイルを読み込む
        with open(f'config/index-settings/{index}.json', 'r') as f:
            settings = json.load(f)
        
        # インデックス作成
        real_index_name = f'{index}-{env}'
        print(f'Create index: {real_index_name}', flush=True)
        es_client.create_index(real_index_name,
            settings = settings,
        )
        es_client.set_aliases(real_index_name, [index])

        # databuildの取得
        databuild = databuild_factory.create(index)

        # dataファイルを読み込んでESを更新
        bulk_str = ''
        bulk_count = 0
        for data_file in os.listdir(f'/data/'):
            with open(f'/data/{data_file}', 'r') as f:
                for line in f:
                    bulk_item: BulkItem = databuild.build(index, line)
                    bulk_str += bulk_item.get_action_line()
                    bulk_str += '\n'
                    bulk_str += bulk_item.get_source_line()
                    bulk_str += '\n'

                    bulk_count += 1
                    if bulk_count >= 50:
                        es_client.bulk(bulk_str)
                        bulk_str = ''
                        bulk_count = 0

        if bulk_count > 0:
            es_client.bulk(bulk_str)
    
    print('Indexer end.', flush=True)

if __name__ == '__main__':
    main()