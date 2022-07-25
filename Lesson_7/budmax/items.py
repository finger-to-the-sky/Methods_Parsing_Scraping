# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, TakeFirst

def process_price(ls: list):
   return [float(ls[0][:-4])]

class BudmaxItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    price_currency = scrapy.Field(output_processor=TakeFirst())
    price_count = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())
