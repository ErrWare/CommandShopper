from Shop import Shop

sprouts = Shop('sprouts',('name','id','base_price',
						  'base_quantity','display_uom',
						  'sale_price','promo_tag',
						  'sale_end_date'))


sprouts.display_cats()

#sprouts.display_items(list(str(i) for i in range(100)))

#sprouts.display_items(('296',))

sprouts.display_shopping_info()