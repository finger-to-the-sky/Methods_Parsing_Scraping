# Написать программу, которая собирает посты из группы https://vk.com/tokyofashion
#
# Будьте внимательны к сайту!
# Делайте задержки, не делайте частых запросов!
#
# 1) В программе должен быть ввод, который передается в поисковую строку по постам группы
# 2) Собирите данные постов:
# - Дата поста
# - Текст поста
# - Ссылка на пост(полная)
# - Ссылки на изображения(если они есть; необязательно)
# - Количество лайков, "поделится" и просмотров поста
#
# 3) Сохраните собранные данные в MongoDB
# 4) Скролльте страницу, чтобы получить больше постов(хотя бы 2-3 раза)
# 5) (Дополнительно, необязательно). Придумайте как можно скроллить "до конца" до тех пор пока посты не перестанут
# добавляться

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pymongo import MongoClient


class vcru():

    def __init__(self, driver):
        self.driver = driver


    def search(self, search_text):
        url = "https://vc.ru/"
        self.driver.get(url)
        search = self.driver.find_elements(By.XPATH, ".//input[contains(@class, 'v-text-input__input')]")
        search[0].click()
        search[0].send_keys(search_text, Keys.ENTER)
        time.sleep(1)


    def save_search(self, MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION, info):
            with MongoClient(MONGO_HOST, MONGO_PORT) as client:
                db = client[MONGO_DB]
                collection = db[MONGO_COLLECTION]
                collection.update_one({"post_name": {"$eq": info['post_name']}}, {"$set": info}, upsert=True)


    def parse_result_search(self):
        find = input('Поиск: ')
        self.search(find)
        self.driver.get(f"https://vc.ru/search/v2/content/relevant?query={find}")

        count = 0
        n = 15
        while count < n:
            authors = self.driver.find_elements(By.XPATH, ".//a[contains(@data-gtm, 'Author Name')]"
                                                     "//div[contains(@class, 'content-header-author__name')]")

            names_posts_list = self.driver.find_elements(By.XPATH, ".//div[contains(@class, 'content-title')]")
            text_post = self.driver.find_elements(By.XPATH, ".//div[contains(@class, 'l-island-a')]//p")
            date = self.driver.find_elements(By.XPATH, ".//time[contains(@class, 'time')]")
            comments = self.driver.find_elements(By.XPATH, ".//a[contains(@class,'comments_counter__count t-link')]")
            link = self.driver.find_elements(By.XPATH, ".//a[contains(@class ,'content-link')]")

            actions = ActionChains(self.driver)
            actions.move_to_element(authors[-1])
            actions.perform()

            time.sleep(2)
            count = len(authors)

            for i in range(n):
                info = {}
                info['author'] = authors[i].text
                info['post_name'] = names_posts_list[i].text
                info['text_post'] = text_post[i].text
                info['date'] = date[i].text
                info['count_comments'] = comments[i].text
                info['link'] = link[i].get_attribute('href')

                self.save_search('localhost', 27017, 'vc_ru', 'result_search', info)
        print('Ваши данные были успешно загруженны')


DRIVER_PATH = './chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(DRIVER_PATH, options=options)

v = vcru(driver)
v.parse_result_search()