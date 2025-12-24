import psycopg2
from psycopg2 import sql
from typing import List, Dict
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_database():
    """Создаёт базу данных, если её нет."""
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    conn.close()

def create_tables():
    """Создаёт таблицы employers и vacancies."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INTEGER
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_id VARCHAR(20) REFERENCES employers(employer_id) ON DELETE CASCADE,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(10),
                url TEXT
            );
        """)
        conn.commit()
    conn.close()

def insert_data(employers: List[Dict], all_vacancies: List[Dict]):
    """Вставляет данные в таблицы."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    with conn.cursor() as cur:
        for emp in employers:
            cur.execute("""
                INSERT INTO employers (employer_id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
            """, (emp["employer_id"], emp["name"], emp["url"], emp["open_vacancies"]))

        for v in all_vacancies:
            cur.execute("""
                INSERT INTO vacancies (vacancy_id, name, employer_id, salary_from, salary_to, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING;
            """, (v["vacancy_id"], v["name"], v["employer_id"],
                  v["salary_from"], v["salary_to"], v["currency"], v["url"]))
        conn.commit()
    conn.close()
