from src.hh_api import HHApi
from src.database import create_database, create_tables, insert_data
from src.db_manager import DBManager

# Список ID интересных компаний (можно найти на hh.ru в URL профиля)
EMPLOYER_IDS = [
    "1740",    # Яндекс
    "1455",    # Сбер
    "3529",    # Тинькофф
    "2180",    # Ozon
    "15478",   # VK
    "84585",   # Kaspersky
    "78638",   # Циан
    "39305",   # Avito
    "80",      # Альфа-Банк
    "1122462"  # Skyeng
]

def main():
    # Шаг 1: Получение данных
    api = HHApi()
    employers = api.get_employers(EMPLOYER_IDS)
    all_vacancies = []
    for emp in employers:
        all_vacancies.extend(api.get_vacancies(emp["employer_id"]))

    # Шаг 2: Создание БД и таблиц
    create_database()
    create_tables()

    # Шаг 3: Загрузка данных
    insert_data(employers, all_vacancies)

    # Шаг 4: Работа с данными
    db = DBManager()

    print("\nКомпании и количество вакансий:")
    for name, count in db.get_companies_and_vacancies_count():
        print(f"{name}: {count} вакансий")

    print(f"\nСредняя зарплата: {db.get_avg_salary()} руб.")

    print("\nВакансии с зарплатой выше средней:")
    for company, title, salary, url in db.get_vacancies_with_higher_salary():
        print(f"{company} — {title} | {salary} руб. | {url}")

    keyword = input("\nВведите ключевое слово для поиска вакансий: ").strip()
    vacancies = db.get_vacancies_with_keyword(keyword)
    if vacancies:
        print(f"\nНайдено {len(vacancies)} вакансий по слову '{keyword}':")
        for company, title, salary, url in vacancies:
            print(f"{company} — {title} | {salary or 'не указана'} руб. | {url}")
    else:
        print("Вакансий не найдено.")

if __name__ == "__main__":
    main()
