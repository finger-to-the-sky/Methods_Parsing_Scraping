import scrapy
from scrapy.http import TextResponse
from ..items import JobparserItem

TEMPLATE_URL = 'https://www.work.ua/ru/jobs-'

class WorkuaSpider(scrapy.Spider):

    name = 'workua'
    allowed_domains = ['work.ua']


    def __init__(self,name_vacantions, max_page, **kwargs):
        super().__init__(*kwargs)

        self.start_urls = [
            TEMPLATE_URL + name_vacantions
        ]
        self.max_page = max_page


    def parse_item(self, response: TextResponse):
        title = response.xpath("//h1[contains(@class, 'add-top')]//text()").getall()
        salary = response.xpath("//b[contains(@class, 'text-black')]//text()").getall()

        if salary == []:
            salary = ['None']

        item = JobparserItem()
        item['title'] = ' '.join(title)
        item['salary'] = salary
        item['url'] = response.url

        yield item


    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):

        items = response.xpath("//div[contains(@class, 'job-link')]")
        for item in items:
            url = item.xpath(".//h2//a//@href").get()
            yield response.follow(url, callback=self.parse_item)

        next_url = response.xpath(
            "//ul[contains(@class, 'pagination')]//li[contains(@class, 'no-style')]//a//@href").get()

        if next_url and page_number <= self.max_page:

            new_kwargs = {
                "page_number": page_number + 1
            }
            yield response.follow(next_url, callback=self.parse, cb_kwargs=new_kwargs)