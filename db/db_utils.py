from pocketbase import PocketBase
from typing import List 
from pocketbase.services.record_service import RecordService
from pocketbase.models.record import Record
from pocketbase.utils import ClientResponseError
from re import search 
from math import ceil 


# global vars & initialization :
config = (
    ('url','text'),
    ('make','text'),
    ('model','text'),
    ('title','text'),
    ('car_price_details','number'),
    ('price_excluding_vat','number'),
    # ('vehicle_detail_additional_detail','json'),

    ('model_year','number'),# change the var type 
    ('vehicle_year','number'), # the the var type 
    ('Mileage','number'), # change the var type 
    ('Regnr','text'), 
    ('Body','text'), 
    ('Gearbox','text'),
    ('engine_size','number'),
    ('Drivetrain','text'),
    ('TopSpeed','text'),
    ('Height','text'),

    ('In_traffic','text'),
    ('Imported_vehicles','text'),
    ('Number_of_seats','number'),
    ('Length','text'),
    ('Width','text'),
    ('Fuel','text'),
    ('Power','text'),
    ('Carbon_dioxide_emissions','text'),

    ('uk_list_space_equipement_detail','text'),
    ('vehicle_detail_equipment_detail',"text"),
    ('new','text')
)


# helper functions : 
def login(user:str, passwd:str) -> PocketBase:
    client = PocketBase('http://127.0.0.1:8090')
    admin_data = client.admins.auth_with_password(user, passwd)
    return client 


def get_schema_object(name:str,type:str='text') -> dict :
    return {
        'id': '',
        'name': name,
        'type': type,
        'system': False,
        'required': False,
        'options': {} ,#if not type=='json' else {"maxSize":2000000},
        'onMountSelect': False,
        'originalName': 'field',
        'toDelete': False
    }


def get_schema_list(makes_models:bool) -> List[dict]:
    return [
        get_schema_object(*schema_obj)
        for schema_obj in (config if not makes_models else config[1:])
    ]


def get_collection_body(collection_name:str,makes_models:bool) -> dict : 
    return {
        'id': '',
        'created': '',
        'updated': '',
        'name': collection_name,
        'type': 'base',
        'system': False,
        'listRule': None,
        'viewRule': None,
        'createRule': None,
        'updateRule': None,
        'deleteRule': None,
        'schema': get_schema_list(makes_models),
        'indexes': [],
        'options': {},
        'originalName': ''
    }


def create_collection(client:PocketBase, collection_name:str,makes_models:bool):
    return client.collections.create(
        get_collection_body(collection_name,makes_models)
    )


def insert_item(collection:RecordService,item:dict):
    collection.create(item)


def update_item(client:PocketBase,collection:RecordService,item:dict):
    collection.update(
        get_id(client,collection,item),
        item
    )


def exist(collection:RecordService,item:dict):
    if item['kind'] == 'makes_models':
        return bool(
                collection.get_list(1,2,{
                    'filter':f'make = "{item["make"]}" && model = "{item["model"]}"'
                }
            ).items
        )
    else :
        return bool(
                collection.get_list(1,2,{
                    'filter':f'url~"{get_url_id(item["url"])}"'
                } 
            ).items
        )
    

def get_url_id(url:str):
    return search('\d+$',url)[0]


def get_id(client:PocketBase,collection:RecordService,item:dict):
    if item['kind'] == 'makes_models':
        return collection.get_list(1,2,{
                        'filter':f'make = "{item["make"]}" && model = "{item["model"]}"'
                    }
                ).items[0].id
    else :
        return collection.get_list(1,2,{
                        'filter':f'url~"{get_url_id(item["url"])}"'
                    } 
                ).items[0].id


def get_total(collection:RecordService,filter:str=None) -> int:
    if filter :
        return ceil(
            collection.get_list(1,1,{'filter':filter}).total_items/500
        )
    else :
        return ceil(
            collection.get_list(1,1).total_items/500
        )


def delete_records(collection:RecordService,records:List[Record]) :
    [
        collection.delete(record.id)
        for record in records
    ]
    

def delete_old_records(collection:RecordService):
    total_pages = get_total(collection,'new="False"')
    for _ in range(1,total_pages+1):
        to_delete_records = collection.get_list(
            1,
            500,
            {'filter':'new = "False"'}
        ).items 
        delete_records(collection,to_delete_records)


def set_the_rest_to_false(collection:RecordService):
    total_pages = get_total(collection)
    for page in range(1,total_pages+1):
        records = collection.get_list(
            page,
            500,
        ).items 
        [
            collection.update(
                record.id,
                {'new':'False'}
            )
            for record in records
        ]

