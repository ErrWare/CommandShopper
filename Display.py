from assets.DictClusterer import DictClusterer
from assets.shoplib import Item, Category
from itertools import zip_longest
import logging
import textwrap
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
        if 'name' not in fields:
            fields.insert(0, 'name')
        elif fields.index('name') != 0:
            fields.remove('name')
            fields.insert(0, 'name')
        col_widths = [len(str(field)) for field in fields]
        items = self.shop.items
        # Only print first 20 items for testing
        items = items[:20]
        for item in items:
            for index, field in enumerate(fields):
                col_widths[index] = max(
                    col_widths[index], len(str(getattr(item, field))))

        max_col_size = 25
        for index, field in enumerate(fields):
                col_widths[index] = min(
                    col_widths[index], max_col_size)
        # Print Header
        col_padding = 4
        padded_width = list(width + col_padding for width in col_widths)

        formatted_col_names = [('{:^'+str(width-1)+'}|').format(getattr(Display.i_columns,field))
                               for field, width in zip(fields, padded_width)]
        header = ''.join(formatted_col_names)
        print(header)

        unf_item_line = '{{{{0:{{0}}<{}}}}}'.format(padded_width[0])
        unf_item_line += ''.join('{{{{{}:{{0}}^{}}}}}'.format(index,width) for index,width in enumerate(padded_width[1:-1],start=1))
        unf_item_line += '{{{{{}:{{0}}>{}}}}}'.format(len(col_widths)-1,padded_width[-1])

        # Print Items
        for item in items:
            #calc entry rows of each col
            col_entries = list(str(getattr(item, field)) for field in fields)
            entry_rows = list(textwrap.wrap(entry,width,subsequent_indent=' ')\
                            for entry, width in zip(col_entries, col_widths)  )
            first_row = True
            for row_entries in zip_longest(*entry_rows, fillvalue=''):
                #for the first row use a '.' filler
                if first_row:
                    row_string = unf_item_line.format('.').format(*row_entries)
                    first_row = False
                #for the rest use a ' ' filler
                else:
                    row_string = unf_item_line.format(' ').format(*row_entries)
                print(row_string)
