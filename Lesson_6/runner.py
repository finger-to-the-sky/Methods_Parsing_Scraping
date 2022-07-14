from jobparser.spiders.workua import WorkuaSpider
from jobparser.spiders.jobsua import JobsuaSpider
from jobparser import settings

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    name_vacantion = input('Наименование вакансии: ')
    max_page = int(input('Количество страниц: '))

    process.crawl(WorkuaSpider, name_vacantion, max_page)
    process.crawl(JobsuaSpider, name_vacantion, max_page)
    process.start()
