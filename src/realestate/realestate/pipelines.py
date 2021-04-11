import codecs
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


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


class CsvSuumoPipeline:
    def __init__(self):
        self.file = open("suumo.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig',
                                        fields_to_export=["name", "property_name", "price", "area", "floor_plan", "age",
                                                          "balcony"])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
