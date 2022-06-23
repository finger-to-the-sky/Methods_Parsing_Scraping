# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя
# (input или argparse), сохранить JSON-вывод в файле, написать функцию, возвращающую (return) спислк репозиториев.

from pprint import pprint
import json
import requests



def get_repos_list(username : str, filename : str):
    responce = requests.get(f'https://api.github.com/users/{username}/repos')
    if responce.status_code == 200:
        with open(f'{filename}.json', 'w') as file:
            json.dump(responce.json(), file, indent=4)
        return responce.json()






