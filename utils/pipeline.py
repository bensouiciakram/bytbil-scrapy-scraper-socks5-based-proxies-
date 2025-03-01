from scrapy.exporters import JsonLinesItemExporter
from pocketbase.utils import ClientResponseError
from scrapy.exceptions import DropItem
from db.db_utils import (
    login,
    create_collection,
    insert_item,
    update_item,
    exist,
    delete_old_records,
    set_the_rest_to_false
)


class MultiExportPipeline:

    def open_spider(self, spider):
        self.makes_models_exporter = JsonLinesItemExporter(
            open('makes_models.jsonl', 'wb'),
            ensure_ascii=False,
            indent=4
        )
        self.cars_exporter = JsonLinesItemExporter(
            open('cars.jsonl', 'wb'),
            ensure_ascii=False,
            indent=4
        )
        self.client = login(
            'bensouiciakram@gmail.com', # username 
            'aaaaaaaaaa' # password
        )
        collection_name = 'makes_models' if spider.makes_models else 'cars'
        try :
            create_collection(self.client,collection_name,spider.makes_models)
        except ClientResponseError as e:
            pass
        self.collection = self.client.collection(collection_name)

    def close_spider(self, spider):
        self.makes_models_exporter.finish_exporting()
        self.cars_exporter.finish_exporting()
        delete_old_records(self.collection)
        set_the_rest_to_false(self.collection)



    def process_item(self, item, spider):        
        if item['kind'] == 'makes_models':
            if not item.get('model'):
                raise DropItem('Missing model')
                return item 
            self.makes_models_exporter.export_item(item)
            if not exist(self.collection,item):
                insert_item(self.collection,item)
            else :
                update_item(self.client,self.collection,item)
        else :
            self.cars_exporter.export_item(item)
            if not exist(self.collection,item):
                insert_item(self.collection,item)
            else :
                update_item(self.client,self.collection,item)
        return item