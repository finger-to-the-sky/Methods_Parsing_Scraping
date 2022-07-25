import scrapy

from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from ..items import BudmaxItem

class BudmaxuaSpider(scrapy.Spider):
    name = 'budmaxua'
    allowed_domains = ['www.budmax.ua']

    def __init__(self, max_page):
        super().__init__(self)
        self.start_urls = [
            f'https://www.budmax.ua/ua/stroitelnye-materialy/uteplitel/penoplast/'
        ]
        self.max_page = max_page

    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        urls = response.xpath("//div[contains(@class, 'text-h4')]//a//@href")

        for item in urls:
            url = item.get()
            yield response.follow(url, callback=self.parse_items)

        next_url = response.xpath("//ul[contains(@class, 'pagination')]//li[last()-1]//a/@href").get()

        if page_number <= self.max_page:
            new_kwargs = {
                'page_number': page_number + 1
            }
            yield response.follow(next_url, self.parse, cb_kwargs=new_kwargs)


    def parse_items(self, response: TextResponse):
        title = response.xpath("//h1[contains(@itemprop, 'name')]//text()").get()
        price = response.xpath("//span[contains(@class, 'priceproduct')]//text()").getall()
        price.pop(0), price.pop(-1)

        curreny = [price[0][-3:]]
        count = [price[1]]

        url = response.url
        characteristics_product = response.xpath("//table[contains(@class, 'table')]//tbody//tr//td//text()").getall()
        image = response.xpath("//meta[contains(@property, 'og:image')]//@content").getall()

        loader = ItemLoader(item= BudmaxItem(), response=response)

        loader.add_value('title', title)
        loader.add_value('price', price)
        loader.add_value('price_currency', curreny)
        loader.add_value('price_count', count)
        loader.add_value('url', url)
        loader.add_value('characteristics', characteristics_product)
        loader.add_value('image', image)

        yield loader.load_item()