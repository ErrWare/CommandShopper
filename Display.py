from assets.DictClusterer import DictClusterer
from assets.shoplib import Item, Category
import logging
logging.basicConfig(level=logging.DEBUG)


class Display:
    i_columns = Item('item',
                      'ID',
                      'base$',
                      'base amt',
                      'unit',
                      'sale$',
                      'sale text',
                      'sale ends',
                      'categories')

    def setShop(self, shop):
        self.shop = shop

    # sort_on id, name, namelength
    def displayCategories(self, sort_on='id'):
        if sort_on == 'id':
            def keyfunc(c): return int(c.ID)
        elif sort_on == 'name':
            def keyfunc(c): return c.name
        elif sort_on == 'len':
            def keyfunc(c): return len(c.name)
        else:
            keyfunc = None
        cats = self.shop.categories
        cats.sort(key=keyfunc)
        max_width = max(len(cat.name) for cat in cats)

        name_header = ' Category Name '
        id_header = ' id '
        max_width = max(max_width, len(name_header))
        unf_header = '{:<'+str(max_width)+'}'+' '*5+'{:>4}'
        print(unf_header.format(name_header, id_header))
        print(unf_header.format('-'*len(name_header), '-'*len(id_header)))
        for cat in cats:
            width = len(cat.name)
            print(cat.name + ' ' + '.' *
                  (5+max_width-width) + '{:>3}'.format(cat.ID))

    def displayItems(self, fields=['name', 'ID']):
        col_widths = [len(str(field)) for field in fields]
        items = self.shop.items
        items = items[:20]
        for item in items:
            for index, field in enumerate(fields):
                col_widths[index] = max(
                    col_widths[index], len(str(getattr(item, field))))
        # Print Header
        formatted_col_names = [('{:^'+str(width)+'}').format(getattr(Display.i_columns,field))
                               for field, width in zip(fields, col_widths)]
        header = (4*' ').join(formatted_col_names)
        print(header)

        # Print Items
        for item in items:
            for field, width in zip(fields, col_widths):
                field_val = str(getattr(item, field))
                print(field_val, (width-len(field_val))*'.', end=4*'.')
            print()

    '''

    '''
    # DATA EXPLORATION

    '''
    def display_shopping_info(self):
        logging.debug('displaying shopping info')
        logging.debug(self.shopping_list)
        clusterer = DictClusterer(
                                 cluster_field='categories',
                                 dic=
                                 {ID : item for ID, item in self._items.items()
                                 if ID in self.shopping_list}
                                 )
        self.display_items(self.get_items(filters=self.shopping_list),
                            fields=[self.item_field.name,
                                    self.item_field.base_price,
                                    self.item_field.base_quantity,
                                    self.item_field.base_unit])

'''
