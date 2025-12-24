import psycopg2
from typing import List, Tuple
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBManager:
    """Класс для взаимодействия с базой данных."""

    def __init__(self):
        self.conn_params = {
            "dbname": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT
        }

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Возвращает список компаний и количество вакансий у каждой."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, COUNT(v.vacancy_id)
                    FROM employers e
                    LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                    GROUP BY e.name
                    ORDER BY COUNT(v.vacancy_id) DESC;
                """)
                return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """Возвращает все вакансии с названием компании, вакансии, зарплатой и ссылкой."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id;
                """)
                return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Возвращает среднюю зарплату по всем вакансиям (по salary_from)."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG(salary_from)
                    FROM vacancies
                    WHERE salary_from IS NOT NULL;
                """)
                result = cur.fetchone()[0]
                return round(result, 2) if result else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        """Возвращает вакансии с зарплатой выше средней."""
        avg = self.get_avg_salary()
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.salary_from > %s
                    ORDER BY v.salary_from DESC;
                """, (avg,))
                return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, str]]:
        """Возвращает вакансии, в названии которых есть keyword (регистронезависимо)."""
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE LOWER(v.name) LIKE %s;
                """, (f"%{keyword.lower()}%",))
                return cur.fetchall()
