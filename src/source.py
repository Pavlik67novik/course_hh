import requests
import json
from abc import ABC, abstractmethod


class AbstractVacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass


class HeadHunterAPI(AbstractVacancyAPI):
    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_vacancies(self, query):
        endpoint = f"{self.base_url}/vacancies"
        params = {"text": query}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            return []


class Vacancy:
    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.salary = salary if salary else "Зарплата не указана"
        self.description = description

    def __str__(self):
        return f"Title: {self.title}\nLink: {self.link}\nSalary: {self.salary}\nDescription: {self.description}"

    def __repr__(self):
        return str(self)



class JSONSaver:
    def __init__(self, file_path):
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        with open(self.file_path, 'a') as file:
            json.dump(vars(vacancy), file)
            file.write('\n')

    def delete_vacancy(self, vacancy):
        # Implement deletion logic here
        pass

    def get_vacancies_by_criteria(self, criteria):
        # Implement retrieval logic here
        pass


def user_interaction():
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = [
        Vacancy(
            item["name"],
            item.get("alternate_url", "No link"),
            item.get("salary", "Зарплата не указана"),
            item["description"]
        )
        for item in hh_vacancies
        if "description" in item
    ]

    #vacancies_list = [Vacancy(item["name"], item["alternate_url"], item["salary"], item["description"]) for item in hh_vacancies]

    filtered_vacancies = filter(lambda v: all(word in v.description for word in filter_words), vacancies_list)

    ranged_vacancies = filter(lambda v: v.salary != "Зарплата не указана" and int(v.salary.split('-')[0]) >= int(salary_range.split('-')[0]) and int(v.salary.split('-')[1].split()[0]) <= int(salary_range.split('-')[1]), filtered_vacancies)

    sorted_vacancies = sorted(ranged_vacancies, key=lambda v: int(v.salary.split('-')[0]), reverse=True)
    top_vacancies = sorted_vacancies[:top_n]

    for vacancy in top_vacancies:
        print(vacancy)


if __name__ == "__main__":
    user_interaction()


