import json
import requests

class EsClient:
    def __init__(self, es_url: str) -> None:
        self.es_url = es_url
    
    def ping(self) -> bool:
        try:
            response = requests.get(self.es_url)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(e)
            return False
    
    def refresh(self) -> bool:
        try:
            response = requests.post(f"{self.es_url}/_refresh")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(e)
            return False
    
    def existIndex(self, index: str) -> bool:
        try:
            response = requests.get(f'{self.es_url}/{index}')
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(e)
            return False
    
    def create_index(self, index: str, settings: dict):
        print(f'[CreateIndex] {index}...', flush=True)
        try:
            response = requests.put(
                f"{self.es_url}/{index}",
                headers={
                    'Content-Type': 'application/json',
                },
                json=settings,
            )
            print(f'[CreateIndex] Response: {response.text}', flush=True)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(e)
            return False
    
    def set_aliases(self, index: str, aliases: list[str]):
        print(f'[SetAliases] {index}...', flush=True)
        try:
            response = requests.post(
                f"{self.es_url}/_aliases",
                headers={
                    'Content-Type': 'application/json',
                },
                json={
                    'actions': [
                        {'add': {'index': index, 'alias': alias}} for alias in aliases
                    ]
                },
            )
            print(f'[SetAliases] Response: {response.text}', flush=True)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(e)
            return False
    
    def bulk(self, bulk_str: str):
        print(f'Do Bulk', flush=True)
        response = requests.post(
            f"{self.es_url}/_bulk",
            headers={
                'Content-Type': 'application/json',
            },
            data=bulk_str,
        )
        #print(f'Bulk success {response.text}', flush=True)
        response.raise_for_status()
