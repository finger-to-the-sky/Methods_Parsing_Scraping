# 1. Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru,yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# - название источника
# - наименование источника
# - ссылку на новость
# - дата публикации
# Нельзя использовать Beautiful Soup.
# 2. Сложить все новости в БД; без дубликатов с обновлениями

# Так как у меня эти российские сайты заблокированы. Я буду брать информацию из этих источников: obozrevatel.com,
# lenta.ru, pravda.com.ua

import time
from pprint import pprint
import requests
from lxml.html import fromstring
from pymongo import MongoClient


class News():

    @staticmethod
    def responce_get(URL: str):
        HEADERS = {'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

        responce = requests.get(URL, headers=HEADERS)
        dom = fromstring(responce.text)
        return dom

    def save_news(self, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION, news):
        with MongoClient(MONGO_HOST, MONGO_PORT) as client:
            db = client[MONGO_DB]
            collection = db[MONGO_COLLECTION]
            collection.update_one({"name": {"$eq": news['name']}}, {"$set": news}, upsert=True)


    def obozrevatel(self):
        date_news = input('Введите дату для получения новостей, например: "27-04-2022": ')
        dom = self.responce_get(f'https://www.obozrevatel.com/main-item/{date_news}.htm')

        NEWS_XPATH = "//article[contains(@class, 'news')]"
        NEWS_LINK = ".//h3//a/@href"

        items = dom.xpath(NEWS_XPATH)
        news_list = [i.xpath(NEWS_LINK) for i in items if i != '']
        for link in news_list:
            dom = self.responce_get(link[0])
            time.sleep(1)
            info = {}

            info['name'] = dom.xpath("//header[contains(@class, 'newsFull_header')]//h1/text()")[0]
            info['link'] = link[0]
            info['date'] = dom.xpath(".//footer//time/@title")[0]
            info['author'] = dom.xpath("//div[contains(@class, 'author')]")[0].xpath(".//a/@href")[0]

            pprint(info)
            self.save_news('localhost', 27017, 'news', 'obozrevatel.com', info)

        print('Запись файлов прошла успешно!')

    def lentaru(self):
        dom = self.responce_get('https://lenta.ru/')

        NEWS_XPATH = "//div[contains(@class,'last24')]//a[contains(@class, 'card-mini')]"
        NEWS_LINK = "./@href"

        items = dom.xpath(NEWS_XPATH)
        news_list = [i.xpath(NEWS_LINK) for i in items]
        for link in news_list:
            dom = self.responce_get(f'https://lenta.ru{link[0]}')
            time.sleep(2)
            info = {}

            info['link'] = f'https://lenta.ru{link[0]}'
            info['name'] = dom.xpath(".//span[contains(@class, 'body__title')]/text()")[0]

            author = dom.xpath(".//a[contains(@class, 'author')]/@href")[0]
            info['author'] = f'https://lenta.ru{author}'
            info['date'] = dom.xpath(".//time[contains(@class, 'topic-header__time')]/text()")[0]

            pprint(info)
            self.save_news('localhost', 27017, 'news', 'lenta.ru', info)
        print('Запись файлов прошла успешно!')


    def pravdaua(self):
        dom = self.responce_get('https://www.pravda.com.ua/rus/news/')

        NEWS_XPATH = ".//div[contains(@class, 'article_content')]"
        NEWS_LINK = ".//a/@href"

        items = dom.xpath(NEWS_XPATH)
        links = [i.xpath(NEWS_LINK)[0] for i in items]
        for link in links:
            if 'https' not in link:
                link = f'https://www.pravda.com.ua{link}'

            dom = self.responce_get(link)
            time.sleep(1)
            info = {}

            info['link'] = link
            if 'life' in link:

                info['name'] = dom.xpath(".//h1[contains(@class, 'page-heading')]/text()")[0]
                info['date'] = dom.xpath("//span[contains(@class, 'data')]/text()")[0]
                info['author'] = dom.xpath("//span[contains(@class, 'autor-name')]/text()")[0]

            else:
                info['name'] = dom.xpath(".//header[contains(@class, 'post')]//h1/text()")[0]
                info['date'] = dom.xpath(".//header[contains(@class, 'post')]//div[contains(@class,'time')]/text()")[0]
                author = dom.xpath(".//header[contains(@class, 'post')]//span[contains(@class, 'post')]//a/text()")

                if author == []:
                    author.append('None')

                info['author'] = author[0]

            pprint(info)
            self.save_news('localhost', 27017, 'news', 'pravda.com.ua', info)
        print('Запись файлов прошла успешно!')




n = News()
n.obozrevatel()
n.lentaru()
n.pravdaua()
