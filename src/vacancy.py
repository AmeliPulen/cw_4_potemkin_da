class Vacancy:
    """Класс для работы с вакансиями (сравнение вакансий, валидация данных)"""

    def __init__(self, title: str, link: str, salary: int,
                 requirement: str) -> None:
        """
        Создание экземпляра класса Vacancy
        """
        if isinstance(title, str):
            self._title = title
        else:
            raise ValueError("Название должно быть строкой.")

        if isinstance(link, str):
            self._link = link
        else:
            raise ValueError("Ссылка должна быть строкой.")

        if isinstance(salary, int) and salary >= 0:
            self._salary = salary
        else:
            raise ValueError("Зарплата должна быть числом.")

        if isinstance(requirement, str):
            self._requirement = requirement
        else:
            raise ValueError("Требования должны быть строкой")


    @property
    def title(self) -> str:
        """
        Возвращает название вакансии
        """
        return self._title


    @property
    def link(self) -> str:
        """
        Возвращает ссылку на вакансию
        """
        return self._link


    @property
    def salary(self) -> int:
        """
        Возвращает значение зарплаты
        """
        return self._salary


    @property
    def requirement(self) -> str:
        """
        Возвращает описание требований
        """
        return self._requirement


    def __eq__(self, other) -> bool:
        """
        Возвращает булев тип при операции сравнения 'равенства'
        """
        if isinstance(other, Vacancy):
            if self._salary is None or other._salary is None:
                return False
            else:
                return self._salary == other._salary
        return False


    def __lt__(self, other) -> bool:
        """
        Возвращает булев тип при операции сравнения 'меньше'
        """
        if isinstance(other, Vacancy):
            if self._salary is None or other._salary is None:
                return False
            else:
                return self._salary < other._salary
        return False


    def __le__(self, other) -> bool:
        """
        Возвращает булев тип при операции сравнения 'меньше или равно'
        """
        if isinstance(other, Vacancy):
            if self._salary is None or other._salary is None:
                return False
            else:
                return self._salary <= other._salary
        return False


    def __gt__(self, other) -> bool:
        """
        Возвращает булев тип при операции сравнения 'больше'
        """
        if isinstance(other, Vacancy):
            if self._salary is None or other._salary is None:
                return False
            else:
                return self._salary > other._salary
        return False


    def __ge__(self, other) -> bool:
        """
        Возвращает булев тип при операции сравнения 'больше или равно'
        """
        if isinstance(other, Vacancy):
            if self._salary is None or other._salary is None:
                return False
            else:
                return self._salary >= other._salary
        return False


    def to_dict(self) -> dict:
        """
        Переводит данные вакансий в тип словаря
        """
        return {
            'title': self._title,
            'link': self._link,
            'salary': self._salary,
            'requirement': self._requirement
        }


    def __repr__(self) -> str:
        """
        Возвращает информацию об объекте класса в режиме отладки
        """
        return f"{self.__class__.__name__}" \
               f"(title={self._title}, link={self._link}, " \
               f"salary={self._salary}, requirement={self._requirement})."