from pymongo import MongoClient
# для использования функции я сделаю импорт из предыдущего урока
from Lesson_2.task_1 import total_result


def only_new_vacantions(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        vacanties = total_result.run()
        db = client[MONGO_DB]
        col_vacanties = db[MONGO_COLLECTION]

        count = 0
        for vacancy in vacanties:

            if col_vacanties.find_one(vacancy):
                pass
            else:
                col_vacanties.insert_one(vacancy)

    print(f'Добавлено {count} новых вакансий')

