from Shop import Shop
from Display import Display
sprouts = Shop('sprouts')


display = Display()
display.setShop(sprouts)
display.displayCategories()

display.displayItems()