import requests 
from scrapy.http.response.html import HtmlResponse
from typing import List 
from math import ceil 
from urllib.parse import quote 
from utils.data_manipulations_utils import (
    format_number
)


# global variabls and initialisations :
primary_fields = {
    'brand':"Märke",
    'model_year':'Årsmodell',
    'Mileage':'Miltal',
    'Regnr':'Regnr',
    'Body':'Karosseri',
    'Fuel':'Drivmedel',
    'Gearbox':'Växellåda',
    'Drivetrain':'Drivhjul',
    'Color':'Färg',
}

additional_fields = {
    'In_traffic':'I trafik',
    'Imported_vehicles':'Importfordon',
    'Number_of_seats':'Antal säten',
    'Length':'Längd',
    'Width':'Bredd',

    'Height':'Höjd',

    'Fuel':'Drivmedel',
    'Power':'Motoreffekt',
    'Carbon_dioxide_emissions':'Koldioxidutsläpp',

    'vehicle_year':'Fordonsår',
    'engine_size':'Motorstorlek',
    'TopSpeed':'Topphastighet',
}

xpaths = {
    'title':'string(//h1)',
    'car_price_details':'//span[@class="car-price-details"]//text()',
    'price_excluding_vat':'//span[@class="price-excluding-vat"]//text()'
}

number_type_fields = (
    'model_year',
    'Mileage',
    'vehicle_year',
    'engine_size'
)

# helper functions :
def extract_makes(response:HtmlResponse) -> List[str]:
    return [
        make 
        for make in response.xpath('//select[@id="Makes"]/option/@value').getall()
        if make.strip() and not make in (
                '--',
                'Car.info',
            )
    ]


def extract_models(response:HtmlResponse) -> List[str]:
    try :
        return [
            model 
            for model in response.json()[0]['value']
            if not model in (
                '--',
                'Car.info',
            )
        ]
    except IndexError:
        return []


def get_total_pages(response:HtmlResponse) -> int:
    try :
        return ceil(
            int(
                response.xpath('//div[contains(@class,"result-count-label")]').re_first('\d+')
            )/24
        )
    except TypeError :
        return 0


def get_cars_urls(response:HtmlResponse) -> List[str]:
    return [
        response.urljoin(car_url)
        for car_url in response.xpath(
            '//h3[@class="uk-text-truncate car-list-header hidden-small-and-below"]//a/@href'
        ).getall()
    ]


def get_detail(fields:dict,xpath_template:str,response:HtmlResponse) -> dict :
    return {
        key:response.xpath(xpath_template.format(value=value)).get().strip()
        if not key in number_type_fields else format_number(response.xpath(xpath_template.format(value=value)).get().strip(),key,response)
        for key,value in fields.items()
    }

def get_primary_detail(car_item:dict,response:HtmlResponse) -> dict :
    car_item.update(
        get_detail(
            primary_fields,
            'string(//dt[contains(text(),"{value}")]/following-sibling::dd)',
            response
        )
    )
    return car_item


def get_car_additional_details(car_item:dict,response:HtmlResponse) -> dict :
    car_item.update(get_detail(
            additional_fields,
            'string(//div[@class="text-gray" and contains(text(),"{value}")]//following-sibling::div[1])',
            response
        )
    )
    return car_item


def update_xpath_fields(car_item:dict,response:HtmlResponse) -> dict :
    car_item.update(
        {
            key:response.xpath(xpath).get() if not 'price' in key else format_number(response.xpath(xpath).get(),key,response)
            for key,xpath in xpaths.items()
        }
    )
    return car_item


def get_uk_list_space(car_item:dict,response:HtmlResponse) -> dict :
    car_item['uk_list_space_equipement_detail'] = '\n'.join(
        response.xpath(
            '//ul[@class="uk-list-space equipment-list"]//li//text()'
        ).getall()
    )
    return car_item


def get_vehicle_detail_equipement_detail(car_item:dict,response:HtmlResponse) -> str :
    car_item['vehicle_detail_equipment_detail'] = response.xpath(
        'string(//div[contains(@class,"vehicle-detail-equipment-detail") and not(descendant::ul)])'
    ).get()
    return car_item 


def check_count(make:str) -> int:
    res = requests.get(
        f'https://www.bytbil.com/api/car/count?Makes={quote(make)}'
    )
    return int(res.text)