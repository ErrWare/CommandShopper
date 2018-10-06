from Shop import Shop

sprouts = Shop('sprouts',('name','id','base_price',
						  'base_quantity','display_uom',
						  'sale_price','promo_tag',
						  'sale_end_date'))


sprouts.display_cats()

#sprouts.display_items(list(str(i) for i in range(100)))

#sprouts.display_items(('296',))
sprouts.get_items(return_size=0,filters=('296',))
sprouts.display_items()
#sprouts.display_shopping_info()
sprouts.display_shopping_info()
#sprouts.display_cats(sprouts.get_cats())