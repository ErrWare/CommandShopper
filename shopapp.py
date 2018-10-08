from Shop import Shop
from Display import Display
sprouts = Shop('sprouts')


display = Display()
display.setShop(sprouts)
display.displayCategories()

display.displayItems()
sprouts.filter_items(filters=['292','293'])
display.displayItems()
sprouts.filter_items(filters=['317'])
display.displayItems()
sprouts.filter_items(filters=['Hass'])
display.displayItems()
sprouts.filter_items(filters=['7080','44295'])
display.displayItems()