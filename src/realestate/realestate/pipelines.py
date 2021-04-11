import codecs
import json


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RealestatePipeline:
    def process_item(self, item, spider):
        return item


class JsonSuumoPipeline:
    # jsonファイルのinput
    def __init__(self):
        self.file = codecs.open("suumo.json", "a", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()