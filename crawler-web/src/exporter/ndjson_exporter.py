import threading
import json
import os

from .export_content import ExportContent

class NdjsonExporter:
    def __init__(self, output_dir: str, output_file_prefix: str, seperate_content_size: int):
        self.output_dir = output_dir.rstrip('/')
        self.output_file_prefix = output_file_prefix
        self.file_counter = 0
        self.content_counter = 0
        self.seperate_content_size = seperate_content_size
        self.lock = threading.Lock()

    def export(self, content: ExportContent) -> None:
        json_content = {
            'url': content.url,
            'title': content.title,
            'content': content.content,
            'attrs': content.attrs
        }

        with self.lock:
            output_file = self.output_dir + '/' + self.output_file_prefix + '_' + str(self.file_counter) + '.ndjson'
            print('output_file=' + output_file)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            mode = 'a' if os.path.exists(output_file) else 'w'
            print('mode=' + mode)
            try:
                with open(output_file, mode) as f:
                    f.write(json.dumps(json_content, ensure_ascii=False) + '\n')
            except Exception as e:
                print(f"Error writing to file: {e}")
        
            self.content_counter += 1
            if self.content_counter >= self.seperate_content_size:
                self.content_counter = 0
                self.file_counter += 1
