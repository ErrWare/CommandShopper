import requests, json

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
		keep_atts_item = ['name','base_price','base_quantity','display_uom']	#uom = unit of measurement
		itemDict[item['id']] = { 'categories':[c['id'] for c in item['categories']]}
		for att in keep_atts_item:
			itemDict[item['id']][att] = item[att]
		# Scrape categories
		for cat in item['categories']:
			catsDict[cat['id']] = cat['name']

'''
with open('sprouts_items.json','w') as file:
	file.write(json.dumps(itemDict))

with open('sprouts_cats.json','w') as file:
	file.write(json.dumps(catsDict))
'''
