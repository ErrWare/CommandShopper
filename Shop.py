import json
import os
import re
from collections import namedtuple
from assets.shoplib import Item, Category
from pprint import pprint


import logging
logging.basicConfig(level=logging.DEBUG)
# logging.disable(level=logging.CRITICAL)


class Shop(object):
    ASSETS_DIR = 'assets'
    CATS_FILE = '_cats.json'
    ITEM_FILE = '_items.json'
    SHOP_FILE = '_shopping_list.json'
    HEADER_FILE = '_headers.json'
    COOKIE_FILE = '_cookies.json'
    URL_FILE = '_url.json'  # unformatted category url
    Item = namedtuple('Item_Fields', ['name', 'id',
                                      'base_price', 'base_quantity',
                                      'base_unit',
                                      'sale_price', 'promo_tag',
                                      'sale_end_date'])

    # item_fields as tuple of (name, base price, base unit, display uom, ..?)
    def __init__(self, name):
        self._filtered_items = []
        self.name = name.lower()
        try:
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.CATS_FILE), 'r') as cat_file:
                self._categories = json.load(cat_file)
                self._categories = {ID: Category(
                    *cat) for ID, cat in self._categories.items()}
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.ITEM_FILE), 'r') as item_file:
                self._items = json.load(item_file)
                self._items = {ID: Item(*val)
                               for ID, val in self._items.items()}
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.HEADER_FILE), 'r') as header_file:
                self.header = json.load(header_file)
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.URL_FILE), 'r') as url_file:
                self.unf_url = json.load(url_file)
        except Exception as e:
            print('Error opening sprouts inventory\nexception: {}'.format(e))
            raise e
        try:
            with open(os.path.join(Shop.ASSETS_DIR, self.name + Shop.SHOP_FILE), 'r') as shopping_list_file:
                self.shopping_list = json.load(shopping_list_file)
        except:
            logging.info('No shopping list detected, creating empty list')
            self.shopping_list = []
        logging.debug('completed {} __init__'.format(self.name))

    '''
    ACCESSING

    '''

    @property
    def items(self):
        return list(self.__dict__.get('_filtered_items', self._items.values()))

    @property
    def categories(self):
        return list(self._categories.values())

    def filter_items(self, filters=None, *, refine=False, _cache={'filters': None}):
        '''
        Set items of interest in shop memory
        '''
        if refine:
            unrefined_items = self._filtered_items
        else:
            unrefined_items = self._items.values()
        if filters != _cache['filters']:
            self._filtered_items = [item for item in unrefined_items if
                                    any(Shop.item_matches(item, f) for f in filters)]
            _cache['filters'] = filters

    '''
    PROCESSING

    '''
    # Marked for deletion
    @staticmethod
    def filter_dic(dic, filters):
        '''
        Return a list of (key, value) pairs that match
        any of the filters given.
        '''
        return [(key, value) for key, value in dic.items()
                for f in filters
                if Shop.item_matches(value, f)]

    @staticmethod
    def item_matches(item, filter_):
        '''
        Return True if item matches filter_
        '''
        if filter_ is None:
            return True
        elif filter_.isdigit():
            return filter_ in item.categories or filter_ == item.ID
        else:
            return re.search(filter_, item.name) is not None
