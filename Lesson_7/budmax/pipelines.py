# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from urllib.parse import urlparse
import re
import scrapy
import os


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'budmax_materyaly'

class BudmaxPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]


    def characteristics_process(self, item):
        l = []
        for i in item:
            j = ''.join(re.findall(r'\w+.', i))
            if j != '':
                l.append(j)

        a = []
        item.clear()
        for i in range(0, len(l)):
            if i % 2 == 0:
                item.append(l[i])

            else:
                q = re.search(r'\d+', l[i])
                if q == []:
                    a.append(l[i])

                else:
                    try:
                        a.append(float(l[i]))
                    except ValueError:
                        a.append(l[i])

        result = dict(zip(item, a))
        return result

    def process_item(self, item, spider):
        item['characteristics'] = self.characteristics_process(item['characteristics'])

        collection = self.db['budmax']
        collection.update_one(item, {'$set': item}, upsert=True)
        return item



class BudmaxImagesPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):

        if item['image']:
            try:
                yield scrapy.Request(item['image'])
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['title']}/" + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        print('images_downloaded')
        return item