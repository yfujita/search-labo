import json

class BulkItem:
    def __init__(self, action: str, index: str, id: str, source: dict):
        self.action = action
        self.index = index
        self.id = id
        self.source = source

    def get_action_line(self) -> str:
        dic = {
            self.action: {
                "_index": self.index,
                "_id": self.id,
            }
        }
        return json.dumps(dic)

    def get_source_line(self) -> str:
        return json.dumps(self.source)