from collections import namedtuple

# standard item info scraped
# if info unavailable -> null in json, or not present
# -> save as None in tuple
Item = namedtuple('Item',
                  [
                      'name',
                      'ID',
                      'base_price',
                      'base_quantity',
                      'uom',
                      'sale_price',
                      'sale_text',
                      'sale_end',
                      'categories'
                  ])
Category = namedtuple('Category',['ID','name'])