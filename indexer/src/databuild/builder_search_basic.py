import json
import base64

from .bulk_item import BulkItem

class SearchBasicBuilder:
    def build(self, index: str, content: str) -> BulkItem:
        json_content = json.loads(content)
        source = {
            'url': json_content['url'],
            'title': json_content['title'],
            'content': json_content['content'],
            'thumbnail': json_content['attrs']['thumbnail'],
        }
        return BulkItem(
            action='index',
            index=index,
            id=base64.b64encode(json_content['url'].encode("utf-8")).decode("utf-8")[:400],
            source=source,)
