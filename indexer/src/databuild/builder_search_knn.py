import json
import base64
import requests
import re


from .bulk_item import BulkItem

class SearchKnnBuilder:
    API_URL = 'http://ml-apis:18081/api/vectorize/bert'

    def build(self, index: str, content: str) -> BulkItem:
        json_content = json.loads(content)
        source = {
            'url': json_content['url'],
            'title': json_content['title'],
            'content': json_content['content'],
            'doc_vector': self.embedding(json_content['title'] + ' ' + json_content['content']),
            'thumbnail': json_content['attrs']['thumbnail'],
        }
        return BulkItem(
            action='index',
            index=index,
            id=base64.b64encode(json_content['url'].encode("utf-8")).decode("utf-8")[:400],
            source=source,)

    def embedding(self, text: str) -> list[float]:
        formatted = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')
        formatted = re.sub(r'\s+', ' ', text)
        response = requests.post(self.API_URL, json={'text': formatted})
        return json.loads(response.text)['vector']