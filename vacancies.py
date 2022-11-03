from api_hh_connect import APIHHConnect
from openpyxl import Workbook
import datetime
from time import perf_counter as pc
from vacancy import Vacancy


class Vacancies:
    name_of_fields = ['id', 'name', 'area', 'salary', 'address', 'response_url', 'published_at', 'created_at',
                      'archived', 'apply_alternate_url', 'alternate_url', 'employer', 'snippet', 'schedule',
                      'working_days', 'working_time_intervals', 'working_time_modes', 'accept_temporary']
    vacancies_array = {}
    number_of_vacancies = 0
    number_of_changes = 0

    def __init__(self):
        self.first_checks_counter = 0
        self.count_archived = 0

    @staticmethod
    def check_inner1(vacancy, field):
        """
        :param vacancy: вакансия - одна из ста полученных в JSON-объекта;
        :param field: поле вакансии, которое необходимо рассмотреть;
        :return: конкретное значение для добавления в двумерный массив.
        """
        if vacancy[field] is not None:
            if isinstance(vacancy[field], list):
                if len(vacancy[field]) == 0:
                    return
            match field:
                case 'id': return vacancy[field]
                case 'name': return vacancy[field]
                case 'area': return vacancy[field]['id']
                case 'salary': return str(vacancy[field]['from']) + ' - ' + str(vacancy[field]['to'])
                case 'address': return vacancy[field]['raw']
                case 'response_url': return vacancy[field]
                case 'published_at': return vacancy[field]
                case 'created_at': return vacancy[field]
                case 'archived': return vacancy[field]
                case 'apply_alternate_url': return vacancy[field]
                case 'alternate_url': return vacancy[field]
                case 'employer': return vacancy[field]['name']
                case 'snippet': return str(vacancy[field]['requirement']) + '\n' + str(vacancy[field]['responsibility'])
                case 'schedule': return vacancy[field]['id']
                case 'working_days': return vacancy[field][0]['id']
                case 'working_time_intervals': return vacancy[field][0]['id']
                case 'working_time_modes': return vacancy[field][0]['id']
                case 'accept_temporary': return vacancy[field]

    def check_all(self, days):
        query = "vacancies"
        now = datetime.date.today()  # сегодняшняя дата
        today = datetime.datetime(now.year, now.month, now.day, 0, 0)  # сегодня в 00:00:00
        date_from = (today - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
        date_to = today.strftime("%Y-%m-%dT%H:%M:%S")
        params = {'specialization': '1', 'date_from': date_from, 'date_to': date_to, 'per_page': 100}
        vacancies = APIHHConnect.connect(query, params)
        print(vacancies['found'])
        if vacancies['found'] > 2000:
            self.separating_by_days(query, params, today, days)

    def separating_by_days(self, query, params, today, days):
        for days_ago in range(days):
            params['date_to'] = (today - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%S")
            params['date_from'] = (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%dT%H:%M:%S")
            params['page'] = None
            vacancies = APIHHConnect.connect(query, params)
            # print(params)
            # print("По дням:" + str(cur_vacancies['found']))
            if vacancies['found'] > 2000:
                self.separating_by_hours(query, params, today, days_ago)
            else:
                cur_len = len(list(self.vacancies_array.keys()))
                self.check_pages(query, params)
                self.number_of_changes += (len(list(self.vacancies_array.keys())) - cur_len)

    def separating_by_hours(self, query, params, today, days_ago):
        cur_day = today - datetime.timedelta(days=days_ago)
        for hours_ago in range(24):
            params['date_to'] = (cur_day - datetime.timedelta(hours=hours_ago)).strftime("%Y-%m-%dT%H:%M:%S")
            params['date_from'] = (cur_day - datetime.timedelta(hours=hours_ago + 1)).strftime("%Y-%m-%dT%H:%M:%S")
            params['page'] = None
            vacancies = APIHHConnect.connect(query, params)
            print(params)
            print("По часам:" + str(vacancies['found']))
            self.first_checks_counter += vacancies['found']
            if vacancies['found'] > 2000:
                print("!!!!!!!!!!!")
                print("!!!ERROR!!!")
                print("!!!ERROR!!!")
                print("!!!ERROR!!!")
                print("!!!!!!!!!!!")
            cur_len = len(list(self.vacancies_array.keys()))
            self.check_pages(query, params)
            self.number_of_changes += (len(self.vacancies_array) - cur_len)

    def check_pages(self, query, params):
        params['page'] = None
        vacancies = APIHHConnect.connect(query, params)
        pages = vacancies['found'] // 100
        if pages > 0:
            for i in range(pages+1):
                params['page'] = i
                vacancies = APIHHConnect.connect(query, params)
                self.get_needed_fields(vacancies)
        else:
            self.get_needed_fields(vacancies)

    def get_needed_fields(self, vacancies):
        """
        :param vacancies: JSON-объект полученный после запроса
        :return: заполнение двумерного массива vacancies_array необходимыми полями.
        """
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            self.number_of_vacancies += 1
            if vacancy['archived']:
                self.count_archived += 1
                continue
            vacancy_to_add = self.create_vacancy(vacancy)
            if vacancy_to_add not in self.vacancies_array.values():
                self.vacancies_array[vacancy_to_add.vacancy_id] = vacancy_to_add

    @staticmethod
    def create_vacancy(vacancy):
        vacancy_id = vacancy['id']
        name = vacancy['name']
        url = vacancy['alternate_url']
        if vacancy['area'] is not None:
            area = vacancy['area']['id']
        else:
            area = None
        if vacancy['address'] is not None:
            address = vacancy['address']['raw']
        else:
            address = None
        if vacancy['employer'] is not None:
            employer = vacancy['employer']['name']
        else:
            employer = None
        if vacancy['salary'] is not None:
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
        else:
            salary_from = None
            salary_to = None
        if vacancy['snippet'] is not None:
            requirement = vacancy['snippet']['requirement']
            responsibility = vacancy['snippet']['responsibility']
        else:
            requirement = None
            responsibility = None

        return Vacancy(vacancy_id, name, area, address, employer, url,
                       salary_from, salary_to, requirement, responsibility)

    def write_in_xlsx(self):
        """
        :return: запись двумерного массива в Excel-таблицу.
        """
        wb = Workbook()
        ws = wb.active
        name_of_fields = ['number', 'id', 'name', 'salary_from', 'salary_to', 'url']
        ws.append(name_of_fields)
        number = 0
        for item in self.vacancies_array.values():
            number += 1
            ws.append([number, item.vacancy_id, item.name, item.salary_from, item.salary_to, item.url])
        wb.save('vacancies2.xlsx')

    def start(self):
        """
        :return: запуск приложения
        """
        self.check_all(1)
        self.write_in_xlsx()
        # print(self.vacancies_array)
        print(self.first_checks_counter)


start = pc()
Vacancies().start()
print(pc()-start)
