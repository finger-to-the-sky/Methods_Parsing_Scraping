# Необходимо собрать информацию о вакансиях на вводимую должность (используем input) с сайтов Superjob(необязательно) и
# HH (обязательно). Приложения должно анализировать неколько страниц сайтов (также вводим через input). Получившийся
# список должен в себе содержать:
#
# - Наименований вакансий.
# - Предлагаемую зарплату (отдельно минимальную и максимальную)
# - Ссылку на саму вакансию.
# - Сайт, откуда была взята вакансия.
#
# Структура данных должна быть одинакова для вакансий с обоих сайтов. Результат сохранить в json файл.


from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json
import re


class workua:

    POSITION = input('Введите наименование вакансии: ')
    PAGE = int(input('Введите номер страницы: '))
    USER_AGENT__ = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'


    def take_soup(self):
        URL = f'https://www.work.ua/ru/jobs-{self.POSITION}?page={self.PAGE}'
        HEADERS = {'User-Agent': self.USER_AGENT__ }

        responce = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(responce.text, 'html.parser')

        return soup


    def name_vacantion(self):
        find_tag = self.take_soup().find_all('h2')
        names = []

        for i in find_tag:
            ls = i.getText(strip=True)

            if ls == 'Понравились результаты поиска?':
                return names
            else:
                names.append(ls)
        return names


    def parse_salary(self):

        find_tag = self.take_soup().find_all('b')
        salaries = []

        for i in find_tag:
            i = i.getText()
            if 'грн' in i or '$' in i or '€' in i or 'руб' in i:
                if '–' in i:
                    min_salary = re.compile(r'\d+\u202f\d+|\d+').findall(i)[0].encode("ascii", "ignore").decode()
                    max_salary = re.compile(r'\u2009\d+\u202f\d+\D').findall(i)[0].encode("ascii","ignore").decode()

                    result = f'{min_salary},{max_salary}'

                else:
                    min_salary = re.compile(r'\d+\u202f\d+|\d+').findall(i)[0].encode("ascii", "ignore").decode()

                    result = f'{min_salary},'

                salaries.append(result)
            else:
                salaries.append('None')

        for i in salaries:
            if  i != 'None':
                salaries.pop(salaries.index(i) + 1)

        return salaries

    def min_salaries(self):
        min_salaries = self.parse_salary()
        for i in min_salaries:
            if i != 'None':
                stry = i[:i.index(',')]
                min_salaries[min_salaries.index(i)] = int(stry)

        return min_salaries

        return min_salaries

    def max_salaries(self):
        max_salaries = self.parse_salary()
        for i in max_salaries:
            if i != 'None':
                stry = i[i.index(',')+1:]

                if stry == '':
                    max_salaries[max_salaries.index(i)] = 'None'

                else:
                    max_salaries[max_salaries.index(i)] = int(stry)
            else:
                stry = 'None'


        return max_salaries


    def find_links(self):

        find_tag = self.take_soup()('h2')
        result = [f'https://www.work.ua{str(i.find("a"))[9:26]}' for i in find_tag]

        return result


    def run(self):
        result_list = []
        names = self.name_vacantion()

        if names == []:
            return 'Не удалось получить наименование вакансий. Пожалуйста, проверьте правильность вводимых данных!'
        else:

            pays_min = self.min_salaries()
            pays_max = self.max_salaries()
            links = self.find_links()

            for i in range(len(names)):
                if pays_min[i] != 'None' and pays_max[i] == 'None':

                    vacanties = {'name': names[i], 'average_salary': pays_min[i], 'link': links[i],
                             'site': 'https://www.work.ua/ru/'}
                else:
                    vacanties = {'name': names[i], 'salary_min': pays_min[i], 'salary_max': pays_max[i],
                                 'link': links[i],
                                 'site': 'https://www.work.ua/ru/'}
                result_list.append(vacanties)

            return result_list

    def create_file(self):
        all_vacantion = self.run()

        with open(f'{self.POSITION}.json', 'a', encoding='utf-8') as file:
            json.dump(all_vacantion, file, indent=4, ensure_ascii=False)


total_result = workua()






# Cделал дополнительную функцию для записи нескольких страниц в один документ, но ее еще нужно доработать.

# def parse_all_pages():
#
#     w = workua()
#     pages = int(input('Теперь введите номер страницы по которую вы хотите получить значения: '))
#     for i in range(w.PAGE, pages+1):
#         arg_2 = w.PAGE = i
#         w.run()
#     print('Done!')
#
# parse_all_pages()