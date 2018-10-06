import json
import os
import re
from DictClusterer import DictClusterer
from collections import namedtuple

import logging
logging.basicConfig(level=logging.DEBUG)
#logging.disable(level=logging.CRITICAL)

class Shop(object):
    ASSETS_DIR  = 'assets'
    CATS_FILE   = '_cats.json'
    ITEM_FILE   = '_items.json'
    SHOP_FILE   = '_shopping_list.json'
    HEADER_FILE = '_headers.json'
    URL_FILE    = '_url.json'    #unformatted category url
    STDItemFields = namedtuple('Item_Fields',['name','id',
                               'base_price','base_quantity',
                               'base_unit',
                               'sale_price','promo_tag',
                               'sale_end_date'])

    #item_fields as tuple of (name, base price, base unit, display uom, ..?)
    def __init__(self, name, 
                 json_item_fields=('name','id','base_price',
                                    'base_quantity','display_uom',
                                   'sale_price','promo_tag','sale_end_date')):
        
        self.name = name.lower()
        self.item_field = Shop.STDItemFields(*json_item_fields)
        try:
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.CATS_FILE),'r') as cat_file:
                self.categories = json.load(cat_file)
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.ITEM_FILE),'r') as item_file:
                self.items = json.load(item_file)
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.HEADER_FILE),'r') as header_file:
                self.header = json.load(header_file)
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.URL_FILE), 'r') as url_file:
                self.unf_url = json.load(url_file)
        except Exception as e:
            print('Error opening sprouts inventory\nexception: {}'.format(e))
            raise e

        try:
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.SHOP_FILE),'r') as shopping_list_file:
                self.shopping_list = json.load(shopping_list_file)
        except:
            print('No shopping list detected, creating empty list')
            self.shopping_list = []
        

        logging.debug('completed {} __init__'.format(self.name))
    
    '''
    DATA EXPLORATION
    
    '''

    #sort_on id or name
    def display_cats(self,displayed_cats=None):
        # Expects iterable of cats in format (cat_id, cat_name)
        if displayed_cats is None:
            displayed_cats = self.get_cats()
        max_name_width = max(len(cat[1]) for cat in displayed_cats)
        for (cat_id, cat_name) in displayed_cats:
            width = len(cat_name)
            print(cat_name + ' ' + '.' * (3+max_name_width-width) + '{:>3}'.format(cat_id))

    def display_items(self,displayed_items=None,fields=['name']):
        if displayed_items is None:
            displayed_items = self.get_items()
        col_widths = [len(field) for field in fields]

        # is there a more pythonic way to do this?
        for ID, item in displayed_items:
            for index, field in enumerate(fields):
                col_widths[index] = max(col_widths[index],len(str(item[field])))
        
        # Print Header
        formatted_col_names = [('{:^'+str(width)+'}').format(field)        \
                               for field, width in zip(fields, col_widths)]
        formatted_col_names.append('itemID')
        print((4*' ').join(formatted_col_names))

        # Print Items
        for ID, item in displayed_items:
            for field, width in zip(fields,col_widths):
                field_val = str(item[field])
                print(field_val, (width-len(field_val))*'.', end=4*'.')
            print(ID)

    def display_shopping_info(self):
        logging.debug('displaying shopping info')
        logging.debug(self.shopping_list)
        clusterer = DictClusterer(
                                 cluster_field='categories',
                                 dic=
                                 {ID : item for ID, item in self.items.items()
                                 if ID in self.shopping_list}
                                 )
        self.display_items(self.get_items(filters=self.shopping_list),
                            fields=[self.item_field.name,
                                    self.item_field.base_price,
                                    self.item_field.base_quantity,
                                    self.item_field.base_unit])
        
    '''
    ACCESSING

    '''

    # sort_on id or name
    def get_cats(self,return_size=25,
                 sort_on='id',
                 _cache={'next_get':0,'cats':None,'order':'id'}):
        restart = _cache['cats'] is None or _cache['order'] != sort_on
        if restart:
            key_func  = (lambda c: int(c[0]))    \
                        if sort_on=='id' else    \
                        (lambda c: c[1])
            cats = list(self.categories.items())
            cats.sort(key=key_func)
            _cache['cats'] = cats
            _cache['order'] = sort_on
        else:
            cats = _cache['cats']

        start_index = _cache['next_get']
        end_index   = start_index+return_size
        gotten_cats = cats[start_index:end_index]
        if end_index >= len(cats):
            end_index = 0
        _cache['next_get'] = end_index
        return gotten_cats

    def get_items(self,filters=None,return_size=25,
                 sort_on='id',
                 _cache={'next_get':0,'items':None,'filters':None}):
        if filters is None and _cache['items'] is None:
            filtered_items = list(self.items.items())
            _cache['items'] = filtered_items

        restart = (filters is not None and _cache['filters'] != filters)    \
                    or                                                      \
                   _cache['items'] is None
        if restart:
            filtered_items = Shop.filter_dic(self.items, filters)
            _cache['items'] = filtered_items
            _cache['filters'] = filters
        else:
            filtered_items = _cache['items']

        start_index = _cache['next_get']
        end_index = start_index + return_size
        gotten_items = filtered_items[start_index:end_index]
        if end_index >= len(filtered_items):
            end_index = 0
        _cache['next_get'] = end_index
        return gotten_items



    '''
    PROCESSING

    '''
    @staticmethod
    def filter_dic(dic, filters):
        return [(key,value) for key, value in dic.items()
                            for f in filters
                            if Shop.item_matches(value, f)]

    @staticmethod                
    def item_matches(item, filter_):
        if filter_.isdigit():
            return filter_ in item['categories'] or filter_ == item['id']
        else:
           return re.search(filter_, item['name']) is not None