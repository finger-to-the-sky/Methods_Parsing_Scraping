# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'jobs'

class JobparserPipeline:

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]

    def process_salary_for_workua(self, salary_str: str):

            if '–' in salary_str:

                salary_list = salary_str.split('–')
                salary_min = re.compile(r'\d+\u202f\d+|\d+').findall(salary_list[0])[0].encode("ascii", "ignore").decode()

                if salary_list[1][-1] != '$':
                    salary_currency = salary_list[1][-3:]
                    salary_max = re.compile(r'\d+\u202f\d+|\d+').findall(salary_list[1][:-3])[0].\
                        encode("ascii", "ignore").decode()

                else:
                    salary_currency = salary_list[1][-1:]
                    salary_max = re.compile(r'\d+\u202f\d+|\d+').findall(salary_list[1][:-1])[0]. \
                        encode("ascii", "ignore").decode()

                return int(salary_min), int(salary_max), salary_currency

            else:

                if salary_str != 'None':
                    if salary_str[-1] != '$':

                        salary_min = re.compile(r'\d+\u202f\d+|\d+').findall(salary_str[:-3])[0].\
                        encode("ascii", "ignore").decode()
                        salary_max = 'None'
                        salary_currency = salary_str[-3:]

                    else:
                        salary_min = re.compile(r'\d+\u202f\d+|\d+').findall(salary_str[:-1])[0].\
                        encode("ascii", "ignore").decode()
                        salary_max = 'None'
                        salary_currency = salary_str[-1:]

                    return int(salary_min), salary_max, salary_currency

                else:
                    return 'None', 'None', 'None'

    def process_salary_for_jobsua(self, salary_str: str):

        if salary_str != 'None':
            if '\xa0+\xa0' in salary_str:

                salary_max = '+ %'
                salary_str = salary_str.replace('.\xa0+\xa0', '')

                if '$' in salary_str:
                    return int(salary_str[:-2].replace(' ', '')), salary_max, salary_str[-1:]

                else:
                    return int(salary_str[:-4].replace(' ', '')), salary_max, salary_str[-3:]

            else:
                salary_max = 'None'

                if '$' in salary_str:
                    return int(salary_str[:-2].replace(' ', '')), salary_max, salary_str[-1:]

                else:
                    return int(salary_str[:-4].replace(' ', '')), salary_max, salary_str[-3:]

        else:
            return 'None', 'None', 'None'

    def process_item(self, item, spider):
        if spider.name == 'jobsua':
            item['salary'], salary_max, salary_currency = self.process_salary_for_jobsua(item['salary'][0])

            if salary_max != '+ %':
                item['salary_currency'] = salary_currency

            else:
                item['salary_max'] = salary_max
                item['salary_currency'] = salary_currency

        else:
            salary_min, salary_max, salary_currency = self.process_salary_for_workua(item['salary'][0])

            item['salary_min'] = salary_min
            item['salary_max'] = salary_max
            item['salary_currency'] = salary_currency
            item.pop('salary')

        item['site'] = spider.name

        mongo_collection = self.db[spider.name]
        mongo_collection.insert_one(item)

        print(item)
        return item
