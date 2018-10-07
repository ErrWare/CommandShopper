import requests, json, re
from shoplib import Item, Category

# field names in received json corresponding to fields in Items
translator = Item(
                  'name',
                  'id',
                  'base_price',
                  'base_quantity',
                  'display_uom',
                  'sale_price',
                  'promo_tag',
                  'sale_end_date',
                  'categories'
                 )

c_translate = Category(
                        'id',
                        'name'
                       )
# Scrape [(catID, catName)] from json item
def get_cat_array(json_item):
    return [Category(cat[c_translate.ID],cat[c_translate.name]) \
            for cat in json_item[translator.categories]]

def get_item_name(json_item):
    name = json_item[translator.name]
    name = re.sub(r',\s1\sEA.*','',name).strip()
    return name


with open('sprouts_url.json','r') as url_file:
    url = json.load(url_file)
with open('sprouts_headers.json','r') as headers_file:
    headers = json.load(headers_file)

# Scrape items
catsDict = {}
itemDict = {}
for i in range(322):    # 322 magic (empirical max index cat)
    res = requests.get(url.format(i),headers=headers)
    try:
        res.raise_for_status()
    except:
        print('Error on id {}'.format(i))
        continue
    res = json.loads(res.text)
    print('id {} count: {}'.format(i,len(res['items'])))
    for item in res['items']:
        # Gather Info from json formatted item
        item_name = get_item_name(item)
        cat_array = get_cat_array(item)
        item_categories = [cat.ID for cat in cat_array]
        all_other_atts = [item.get(field, None) for field in translator[1:-1]]
        item_tuple = Item(item_name,*all_other_atts, item_categories)
        # Save to dicts
        itemDict[item_tuple.ID] = item_tuple
        for cat in cat_array:
            catsDict[cat.ID] = cat

# Save dicts to files
with open('sprouts_items.json','w') as file:
    file.write(json.dumps(itemDict))

with open('sprouts_cats.json','w') as file:
    file.write(json.dumps(catsDict))

