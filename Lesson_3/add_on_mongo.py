from pymongo import MongoClient
# для использования функции я сделаю импорт из предыдущего урока
from Lesson_2.task_1 import total_result


def add_on_mongo(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:

        vacanties = total_result.run()
        db = client[MONGO_DB]
        col_vacanties = db[MONGO_COLLECTION]

        for vacancy in vacanties:
            col_vacanties.insert_one(vacancy)

    print(f'Добавлено {len(vacanties)} новых вакансий')

a = add_on_mongo('localhost', 27017, 'workua', 'vacantions')