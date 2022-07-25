from urllib import parse
from urllib.parse import quote, quote_plus
from budmax.spiders.budmaxua import BudmaxuaSpider
from budmax import settings

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


# https://www.budmax.ua/ua/search/?search=%D0%BF%D0%B5%D0%BD%D0%BE%D0%BF%D0%BB%D0%B0%D1%81%D1%82
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    max_page = 3
    process.crawl(BudmaxuaSpider, max_page)
    process.start()