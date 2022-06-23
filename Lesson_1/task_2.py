# Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент
# для города, название которого получается через input.



# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}


import json
import requests
from pprint import pprint

key = ''
name = input('Enter name your city: ')

def weather_city(name : str, key: str):
    responce = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&appid={key}')
    if responce.status_code == 200:
        return responce.json()


pprint(weather_city(name, key))