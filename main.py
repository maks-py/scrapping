"""
Скраппинг карточек объявлений на основе урока https://youtu.be/qkrgVz60dck
"""
from bs4 import BeautifulSoup
import requests
from requests import get
import time
import random



def scrap(kwargs:dict):
    """
    Функция скраппинга карточек товаров
    kwargs - словарь с параметрами скраппинга, такими как типы тегов и названия классов 
    в обрабатываемом html файле
    """
    products = []
    count = 1
    # Получение параметров из kwargs
    page_count = kwargs.get('page_count')
    url_part = kwargs.get('url')
    # тег карточки товара
    product_tag = kwargs.get('product_card').get('tag')
    # класс карточки товара
    product_class = kwargs.get('product_card').get('class')


    # Ищу карточки товара на каждой странице сайта
    while count <= page_count:
        url = url_part + str(count)

        print(f"parse {url}")
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        # Все карточки соответствующие параметрам поиска
        card_data = html_soup.find_all(product_tag, class_=product_class)

        # Сплю рандомное время
        if card_data:
            products.extend(card_data)
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            print(scaled_value)
            time.sleep(scaled_value)
        else:
            print('all parsed')
            break
        count += 1


    print(f"Len of products {len(products)}\n")
    product_length = int(len(products)) - 1
    count = 0
    str_res = []

    # Получение параметров полей карточки из kwargs
    fields = list(kwargs.get('fields'))
    if not fields:
        return None

    # По всем карточкам
    while count <= product_length:
        product_card = products[int(count)]

        product_string = ''
        # По всем указанным полям карточки
        for field in fields:
            field_tag = kwargs.get('fields')[field]['tag']
            field_class = kwargs.get('fields')[field]['class']

            field_text = product_card.find(field_tag, {"class": field_class})
            if not field_text:
                break
            
            field_text = str(field_text.text)
            # В строку собирается название поля и его значение
            product_string += "{}: {} ".format(field, field_text) 

        if product_string:
            product_string = product_string.replace("\xa0", ' ')
            # Строка добавляется в список
            str_res.append(product_string)
            print(product_string)

        count += 1

    return  str_res


def write_file(ofile:str, strings:list):
    """
    Запись строк strings в ofile файл
    """
    count = 0
    with open(ofile, 'w') as f:
        while count < len(strings):
            f.write(strings[count] + "\n")
            count += 1


def load_json_as_dict(file:str):
    """
    Чтение json файла
    """
    import json
    try:
        with open (file) as fn:
             obj = json.load(fn)
        return obj
    except FileNotFoundError:
        return None


# Из параметров командной строки получаю файл параметров скраппинга (*.json)
# и название выходного файла
if __name__ == '__main__':
    import sys
    out = []
    ls = sys.argv
    print(ls)
    
    #Args - 1 - params file, 2 - out file
    if len(ls) == 3:
        params = load_json_as_dict(ls[1])
        if params:
            strings = scrap(params)
            write_file(ofile=ls[2], strings=strings)
