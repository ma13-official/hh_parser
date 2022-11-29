import os
import threading

from api_hh_connect import APIHHConnect
import datetime
from time import perf_counter as pc

from dirs import Dirs
from jsons import JSONs
from vacancy import Vacancy
from parameters_for_queries import ParametersForQueries
from csvs import CSVs
import logging


class Vacancies:
    vacancies_array = {}
    currencies = {}
    every_day_checks_counter, every_hour_checks_counter, count_duplicates = [0 for _ in range(3)]
    json_urls = []

    def check_all(self, days):
        query = "vacancies"
        now = datetime.date.today()  # сегодняшняя дата
        today = datetime.datetime(now.year, now.month, now.day, 0, 0)  # сегодня в 00:00:00
        date_from = (today - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
        date_to = today.strftime("%Y-%m-%dT%H:%M:%S")
        params = {'specialization': '1', 'date_from': date_from, 'date_to': date_to, 'per_page': 100}
        Dirs.make_dir('C:/Users/mi/work/hh_parser/vacancies/', today.strftime("%Y-%m-%d"))
        vacancies = APIHHConnect.connect(query, params)
        logging.info(f"Founded {str(vacancies['found'])} vacancies")
        if vacancies['found'] > 2000:
            self.separating_by_days(query, params, today, days)
        else:
            logging.error(f"From {params['date_from']} to {params['date_to']} founded more than 2000 vacancies!")

    def separating_by_days(self, query, params, today, days):
        for days_ago in range(days):
            self.vacancies_array = {}
            params['date_to'] = (today - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%S")
            params['date_from'] = (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%dT%H:%M:%S")
            params['page'] = None
            vacancies = APIHHConnect.connect(query, params)
            founded = vacancies['found']
            logging.info(f"{params['date_from'][:10]} founded {founded} vacancies")
            self.every_day_checks_counter += vacancies['found']
            Dirs.make_dir('C:/Users/mi/work/hh_parser/vacancies/',
                          (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%d"))
            if vacancies['found'] > 2000:
                self.separating_by_hours(query, today, days_ago)
            else:
                self.check_pages(query, params)
            date = (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%d")
            first_check = not os.path.exists(
                'C:/Users/mi/OneDrive - ITMO UNIVERSITY/work/hh_parser/vacancies_per_day/' + date + '.xlsx')
            CSVs.write_in_csv(self.vacancies_array, date)
            CSVs.write_jsons_in_csv(self.json_urls, date)
            CSVs.check_len_csv(date, founded, first_check)
            self.json_urls = []

    def separating_by_hours(self, query, today, days_ago):
        cur_day = today - datetime.timedelta(days=days_ago)
        for hour in range(0, 24, 4):
            self.threads(query, cur_day, hour)

    def threads(self, query, cur_day, hour):
        threads = []
        for x in range(4):
            params = {'specialization': '1', 'per_page': 100,
                      'date_from': (cur_day - datetime.timedelta(hours=hour + x + 1)).strftime("%Y-%m-%dT%H:%M:%S"),
                      'date_to': (cur_day - datetime.timedelta(hours=hour + x)).strftime("%Y-%m-%dT%H:%M:%S")}
            t = threading.Thread(target=self.query_by_hours, args=(query, params))
            threads.append(t)
            t.start()
            params = {}
        for t in threads:
            t.join()

    def query_by_hours(self, query, params):
        vacancies = APIHHConnect.connect(query, params)
        logging.info(f"From {params['date_from']} to {params['date_to']} founded {str(vacancies['found'])} vacancies")
        self.every_hour_checks_counter += vacancies['found']
        if vacancies['found'] > 2000:
            logging.error(f"From {params['date_from']} to {params['date_to']} founded more than 2000 vacancies!")
        cur_len = len(list(self.vacancies_array.keys()))
        self.check_pages(query, params)

    def check_pages(self, query, params):
        # print(params)
        params['page'] = None
        vacancies = APIHHConnect.connect(query, params)
        pages = vacancies['found'] // 100
        if pages > 0:
            for i in range(pages + 1):
                params['page'] = i
                vacancies = APIHHConnect.connect(query, params)
                JSONs.save_vacancies_json(vacancies, params)
                self.get_needed_fields(vacancies)
        else:
            JSONs.save_vacancies_json(vacancies, params)
            self.get_needed_fields(vacancies)

    def get_needed_fields(self, vacancies):
        """
        :param vacancies: JSON-объект полученный после запроса
        :return: заполнение двумерного массива vacancies_array необходимыми полями.
        """
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            if vacancy['archived']:
                print(1)
                continue
            vacancy_to_add = Vacancy.create_vacancy(vacancy, self.currencies)
            if CSVs.check_csv(vacancy_to_add):
                self.vacancies_array[vacancy_to_add.vacancy_id] = vacancy_to_add
                self.json_urls.append([vacancy_to_add.vacancy_id, vacancy_to_add.url_json])
                CSVs.create_csv(vacancy_to_add)
            else:
                self.count_duplicates += 1

    def start(self, check_all=True, number_of_days=1, upload_jsons=False):
        """
        :return: запуск приложения
        """
        logging.basicConfig(level=logging.INFO,
                            filename=f"./vacancies_logs/"
                                     f"{datetime.datetime.today().strftime('%Y-%m-%dT%H--%M--%S')}.log",
                            filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        if check_all:
            logging.info(f"Checking of last {number_of_days} days started.")
            self.currencies = ParametersForQueries.get_currencies()
            self.check_all(number_of_days)
            logging.info(self.every_day_checks_counter)
            logging.info(self.every_hour_checks_counter)
            logging.info(self.count_duplicates)
        if upload_jsons:
            logging.info("Upload of single vacancies JSONs started.")
            JSONs.upload_all_jsons()


start = pc()
Vacancies().start(check_all=False,
                  number_of_days=30,
                  upload_jsons=True)
logging.info(f"Program works {round(pc() - start)} seconds")
