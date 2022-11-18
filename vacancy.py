import json
import os
from openpyxl.workbook import Workbook
from api_hh_connect import APIHHConnect


class Vacancy:
    def __init__(self, vacancy_id, name, area, address, employer, url_hh, url_json, published_at, created_at,
                 salary_from=None, salary_to=None, requirement=None, responsibility=None,
                 schedule=None, working_days=None, working_time_intervals=None, working_time_modes=None,
                 accept_temporary=None):
        self.vacancy_id = vacancy_id
        self.name = name
        self.area = area
        self.address = address
        self.employer = employer
        self.url_hh = url_hh + ' '
        self.url_json = url_json + ' '
        self.published_at = published_at
        self.created_at = created_at
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.requirement = requirement  # отрывки
        self.responsibility = responsibility
        self.schedule = schedule
        self.working_days = working_days
        self.working_time_intervals = working_time_intervals
        self.working_time_modes = working_time_modes
        self.accept_temporary = accept_temporary
        self.create_csv()
        # self.get_json()

    @staticmethod
    def create_vacancy(vacancy, currencies):
        vacancy_id = vacancy['id']
        name = vacancy['name']
        url_hh = vacancy['alternate_url']
        url_json = vacancy['url']
        published_at = vacancy['published_at']
        created_at = vacancy['created_at']
        accept_temporary = vacancy['accept_temporary']
        fields = ['area', 'address', 'employer', 'salary', 'snippet']
        area, address, employer, salary_from, salary_to, requirement, responsibility, schedule, \
        working_days, working_time_intervals, working_time_modes = [None for _ in range(11)]
        for field in fields:
            if vacancy[field] is not None:
                if isinstance(vacancy[field], list):
                    if len(vacancy[field]) == 0:
                        continue
                match field:
                    case 'area':
                        area = vacancy['area']['id']
                    case 'address':
                        address = vacancy['address']['raw']
                    case 'employer':
                        employer = vacancy['employer']['name']
                    case 'salary':
                        if salary_from is None:
                            salary_from = None
                            continue
                        if salary_to is None:
                            salary_to = None
                            continue
                        salary_from = vacancy['salary']['from'] / currencies[vacancy['salary']['currency']]
                        salary_to = vacancy['salary']['to'] / currencies[vacancy['salary']['currency']]
                        if vacancy['salary']['gross']:
                            salary_from *= 0.87
                            salary_to *= 0.87
                    case 'snippet':
                        requirement = vacancy['snippet']['requirement']
                        responsibility = vacancy['snippet']['responsibility']
                    case 'schedule':
                        schedule = vacancy[field]['id']
                    case 'working_days':
                        working_days = vacancy[field][0]['id']
                    case 'working_time_intervals':
                        working_time_intervals = vacancy[field][0]['id']
                    case 'working_time_modes':
                        working_time_modes = vacancy[field][0]['id']
        return Vacancy(vacancy_id, name, area, address, employer, url_hh, url_json, published_at, created_at,
                       salary_from, salary_to, requirement, responsibility, schedule, working_days,
                       working_time_intervals, working_time_modes, accept_temporary)

    def create_csv(self):
        past_path = os.getcwd()
        PATH = 'C:/Users/mi/work/hh_parser/vacancies/'
        wb = Workbook()
        ws = wb.active
        name_of_fields = ['vacancy_id', 'name', 'area', 'address', 'employer', 'url_hh', 'url_json',
                          'published_at', 'created_at', 'salary_from', 'salary_to', 'requirement', 'responsibility',
                          'schedule', 'working_days', 'working_time_intervals', 'working_time_modes',
                          'accept_temporary']
        ws.append(name_of_fields)
        row = []
        for value in self.__dict__.values():
            row.append(value)
        ws.append(row)
        date = self.published_at[:10]
        wb.save(PATH + date + '/' + str(self.vacancy_id) + '.csv')

    def get_json(self):
        PATH = 'C:/Users/mi/work/hh_parser/vacancies_jsons/'
        vacancy = APIHHConnect.connect('vacancies/' + self.vacancy_id)
        date = self.published_at[:10]
        os.chdir(PATH)
        if not os.path.isdir(date):
            os.mkdir(date)
        os.chdir(date)
        with open(PATH + date + '/' + str(self.vacancy_id) + '.json', 'w') as outfile:
            json.dump(vacancy, outfile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

    @staticmethod
    def check_csv(vacancy):
        return not os.path.exists('C:/Users/mi/work/hh_parser/vacancies/' + vacancy.published_at[:10] + '/'
                                  + str(vacancy.vacancy_id) + '.csv')
