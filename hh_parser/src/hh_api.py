import requests
from typing import List, Dict, Any

class HHApi:
    """Класс для взаимодействия с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_employers(self, employer_ids: List[str]) -> List[Dict[str, Any]]:
        """Получает информацию о работодателях по их ID."""
        employers = []
        for emp_id in employer_ids:
            url = f"{self.base_url}/employers/{emp_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                employers.append({
                    "employer_id": data["id"],
                    "name": data["name"],
                    "url": data["alternate_url"],
                    "open_vacancies": data["open_vacancies"]
                })
        return employers

    def get_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Получает вакансии для одного работодателя."""
        url = f"{self.base_url}/vacancies?employer_id={employer_id}&per_page=100"
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.json()
        vacancies = []
        for v in data.get("items", []):
            salary = v.get("salary")
            from_salary = to_salary = None
            currency = "RUR"
            if salary:
                from_salary = salary.get("from")
                to_salary = salary.get("to")
                currency = salary.get("currency", "RUR")
            vacancies.append({
                "vacancy_id": v["id"],
                "name": v["name"],
                "employer_id": employer_id,
                "salary_from": from_salary,
                "salary_to": to_salary,
                "currency": currency,
                "url": v["alternate_url"]
            })
        return vacancies
