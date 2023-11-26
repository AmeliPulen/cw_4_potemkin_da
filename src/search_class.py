import os
import requests

from abc import ABC, abstractmethod


class ErrorResponse(Exception):
    """Класс исключения для ошибки запроса"""

    def __init__(self, *args) -> None:
        """
        Конструктор класса ErrorResponse.
        """
        self.message = args[0] if args else "Ошибка выполнения запроса"

    def __str__(self) -> str:
        """Возвращает строковое сообщение об ошибке"""
        return self.message


class SearchEngine(ABC):
    """Абстрактный класс для наследования классов HeadHunterAPI и SuperJobAPI"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, search_query, search_area):
        pass


class HeadHunterAPI(SearchEngine):
    """Класс поиска вакансий на сайте HeadHunter"""

    def __init__(self):
        """
        Создание экземпляра класса
        """
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str, search_area: int) -> list[dict]:
        """
        Выполнение запроса по параметрам пользователя
        """
        params = {
            "text": search_query,
            "area": search_area,
            "per_page": 100,
            "only_with_salary": True,
            "search_fields": "name"
        }

        # Выполнение запроса
        response = requests.get(self.url, params=params)

        # Проверка запроса на ошибку
        if response.status_code == 200:
            data_vacancy = response.json()['items']
            return self.data_organize(data_vacancy)
        else:
            raise ErrorResponse("Ошибка при выполнении запроса: ",
                                response.status_code)

    @staticmethod
    def data_organize(data_vacancy) -> list[dict]:
        """
        Формирование списка словарей вакансий
        """
        vacancies = []
        for vacancy in data_vacancy:
            title = vacancy['name']
            link = vacancy['alternate_url']
            requirement = vacancy['snippet'].get('requirement', None)
            salary_from = vacancy['salary'].get('from', None)
            salary_to = vacancy['salary'].get('to', None)

            # Проверка заработной платы на границы
            if salary_from and salary_to:
                salary = min(salary_from, salary_to)
            else:
                salary = salary_from or salary_to

            # Проверка наличие требований
            if requirement:
                requirement = requirement.lower()
            else:
                requirement = 'Нет данных.'

            # Формирование списка данных
            vacancies.append({
                'title': title,
                'link': link,
                'salary': salary,
                'requirement': requirement
            })

        return vacancies


class SuperJobAPI(SearchEngine):
    """Класс поиска вакансий на сайте SuperJob"""

    def __init__(self):
        """
        Создание экземпляра класса
        """
        self.url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancies(self, search_query: str, search_area: int) -> list[dict]:
        """
        Выполнение запроса по параметрам пользователя
        """
        headers = {"X-Api-App-Id": os.environ["SUPERJOB_API_KEY"]}
        params = {
            "keyword": search_query,
            "page": 0,
            "count": 10,
            "town": search_area
        }

        # Выполнение запроса
        response = requests.get(self.url, headers=headers, params=params)

        # Проверка запроса на ошибку
        if response.status_code == 200:
            data_vacancy = response.json()['objects']
            return self.data_organize(data_vacancy)
        else:
            raise ErrorResponse(f"Ошибка при выполнении запроса: {response.status_code}")

    @staticmethod
    def data_organize(data_vacancy) -> list[dict]:
        """
        Формирование списка словарей вакансий
        """
        vacancies = []
        for vacancy in data_vacancy:
            title = vacancy['profession']
            link = vacancy['link']
            salary_from = vacancy.get('payment_from', None)
            salary_to = vacancy.get('payment_to', None)
            requirement = vacancy.get('candidat', None)

            # Проверка заработной платы на границы
            if salary_from and salary_to:
                salary = min(salary_from, salary_to)
            else:
                salary = salary_from or salary_to

            # Проверка наличие требований
            if requirement:
                requirement = requirement.lower()
            else:
                requirement = 'Нет данных.'

            # Проверка заработной платы на нулевые (на самом деле больше 1000) значения
            if salary > 1000:
                vacancies.append({
                    'title': title,
                    'link': link,
                    'salary': salary,
                    'requirement': requirement
                })

        return vacancies
