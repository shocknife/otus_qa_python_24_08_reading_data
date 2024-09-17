from csv import DictReader
import json
from files_data import get_path


def distribute_books(books_file, users_file, result_file):
    # Чтение книг из файла

    with open(
        get_path(filename=f"{books_file}"), mode="r", newline="", encoding="utf-8"
    ) as bf:
        reader = DictReader(bf)

        count_books = 0
        list_books = []
        for row in reader:
            list_books.append(row)

    result_list_books = []

    for i in list_books:
        result_list_books.append(
            {
                "Title": i["Title"],
                "Author": i["Author"],
                "Pages": i["Pages"],
                "Genre": i["Genre"],
            }
        )
        count_books += 1

    # Чтение пользователей из json-файла с первоначальными данными

    with open(
        get_path(filename=f"{users_file}"), mode="r", encoding="utf-8"
    ) as srcfile:
        data = json.load(srcfile)

    # собираем нужные нам данные из записей
    count_users = 0
    result_list_users = []

    for i in data:
        if i["isActive"]:
            result_list_users.append(
                {
                    "name": i["name"],
                    "gender": i["gender"],
                    "address": i["address"],
                    "age": i["age"],
                }
            )
            count_users += 1

    # Распределение книг между пользователями
    num_users = len(result_list_users)
    num_books = len(result_list_books)

    books_per_user = num_books // num_users
    remaining_books = num_books % num_users

    index = 0

    # Распределение книг
    for user in range(num_users):
        result_list_users[user]["books"] = [
            result_list_books[index : index + books_per_user]
        ]
        index += books_per_user

    # Распределение оставшихся книг
    for i in range(remaining_books):
        result_list_users[i]["books"] = [result_list_books[index]]
        index += 1

    # Запись результата в JSON файл
    with open(get_path(filename=f"{result_file}"), "w", encoding="utf-8") as f:
        json.dump(result_list_users, f, ensure_ascii=False, indent=4)


# Пример использования функции
distribute_books("books.csv", "users.json", "result.json")
