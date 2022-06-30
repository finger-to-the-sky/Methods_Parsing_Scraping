from pprint import pprint
from pymongo import MongoClient
# для использования функции я сделаю импорт из предыдущего урока



def find_salary_vacantions(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION,):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        col_vacanties = db[MONGO_COLLECTION]
        size_payment = input('Запущена функция поиска вакансий. Укажите зарплату, больше которой вы хотите '
                             'видеть на экране.\nЕсли вы хотите отобразить вакансии без зарплат, поставьте прочерк -. '
                             'Введите сумму: ')
        if size_payment == '-':
            cursor = col_vacanties.find({'salary_min': 'None'})
        elif size_payment != '-':
            try:
                cursor = col_vacanties.find({'$or':
                                                 [
                                                     {'salary_min': {'$gt': int(size_payment)}},
                                                     {'average_salary': {'$gt':int(size_payment)}}
                                                      ]
                })
                cursor2 = col_vacanties.find({'average_salary': {'$gt':int(size_payment)}})

            except ValueError:
                print('Неверно введены данные!')
                return None

        for doc in cursor:
            pprint(doc)


f = find_salary_vacantions('localhost', 27017, 'workua', 'vacantions')
















# if payment_size:
#     cursor = col_vacanties.find({
#         '$and': [
#             {'salary': {'#ne': None}},
#             {'$or'[
#                  {'salary': {'$gte': int(payment_size)}},
#                  {'salary': {'$gte': int(payment_size)}}
#              ]}
#         ]
#     })
#     return list(cursor)
# else:
#     cursor = col_vacanties.find({'$or': [{'salary': None}, {'salary': {'$type': 'string'}}]})
#     return list(cursor)