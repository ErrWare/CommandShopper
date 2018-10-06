import requests, json, re
from collections import namedtuple

Item = namedtuple('Item',
                  [
                      'name',
                      'ID',
                      'base_price',
                      'base_quantity',
                      'uom',
                      'categories',
                      'sale_price',
                      'sale_text',
                      'sale_end'
                  ])

translator = Item(
                  'name',
                  'id',
                  'base_price',
                  'base_quantity',
                  'categories',
                  'display_uom',
                  'sale_price',
                  'promo_tag',
                  'sale_end_date'
                 )
# set item limit higher when scraping
with open('sprouts_url.json','r') as url_file:
    url = json.load(url_file)
with open('sprouts_headers.json','r') as headers_file:
    headers = json.load(headers_file)

# Scrape items
catsDict = {}
itemDict = {}
for i in range(322):
    res = requests.get(url.format(i),headers=headers)
    try:
        res.raise_for_status()
    except:
        print('Error on id {}'.format(i))
        continue
    res = json.loads(res.text)
    print('id {} count: {}'.format(i,len(res['items'])))
    for item in res['items']:
        # Scrape Items
        keep_atts_item = ['name','base_price','base_quantity','display_uom','id']    #uom = unit of measurement
        itemDict[item['id']] = { 'categories':[c['id'] for c in item['categories']]}
        item['name'] = re.sub(',\s1\sEA.*','',item['name']).strip()
        for att in keep_atts_item:
            itemDict[item['id']][att] = item[att]
        # Scrape categories
        for cat in item['categories']:
            catsDict[cat['id']] = cat['name']


with open('sprouts_items.json','w') as file:
    file.write(json.dumps(itemDict))

with open('sprouts_cats.json','w') as file:
    file.write(json.dumps(catsDict))

