import json
import os
from openpyxl.workbook import Workbook
from api_hh_connect import APIHHConnect
from csvs import CSVs


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
                        if vacancy['salary']['to'] is not None:
                            salary_to = vacancy['salary']['to'] / currencies[vacancy['salary']['currency']]
                            if vacancy['salary']['gross']:
                                salary_to *= 0.87
                        if vacancy['salary']['from'] is not None:
                            salary_from = vacancy['salary']['from'] / currencies[vacancy['salary']['currency']]
                            if vacancy['salary']['gross']:
                                salary_from *= 0.87
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

# v = Vacancy(1,2,3,4,5,'6','7',8,9)
# print(v.__dict__.values())