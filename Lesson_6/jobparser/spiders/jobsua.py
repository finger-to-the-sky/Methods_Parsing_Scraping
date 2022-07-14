import scrapy
from scrapy.http import TextResponse
from ..items import JobparserItem

TEMPLATE_URL = 'https://jobs.ua/vacancy/rabota-'


class JobsuaSpider(scrapy.Spider):
    name = 'jobsua'
    allowed_domains = ['jobs.ua']

    def __init__(self,name_vacantions, max_page, **kwargs):
        super().__init__(**kwargs)

        self.start_urls = [
            TEMPLATE_URL + name_vacantions
        ]
        self.max_page = max_page

    def parse_item(self, response: TextResponse):
        title = response.xpath("//h1[contains(@class, 'full-title')]//text()").getall()
        salary = response.xpath("//div[contains(@class, 'full__pay')]//text()").getall()

        if salary == []:
            salary = ['None']

        else:
            salary = [''.join(salary)[:-1]]

        item = JobparserItem()
        item['title'] = title[0]
        item['salary'] = salary
        item['url'] = response.url

        yield item


    def parse(self, response: TextResponse, page_number: int = 1, **kwargs):
        items = response.xpath("//a[contains(@class, 'vacancy__top__title')]")

        for item in items:
            url = item.xpath(".//@href").get()
            yield response.follow(url, callback=self.parse_item)

        next_url = response.xpath("//a[contains(@class, 'pager__arrow')]//@href").get()

        if next_url and page_number <= self.max_page:
            new_kwargs = {
                'page_number': page_number + 1,
            }
            yield response.follow(next_url, callback=self.parse, cb_kwargs=new_kwargs)