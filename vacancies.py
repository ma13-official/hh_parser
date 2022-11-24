import threading

from api_hh_connect import APIHHConnect
import datetime
from time import perf_counter as pc

from dirs import Dirs
from jsons import JSONs
from vacancy import Vacancy
from parameters_for_queries import ParametersForQueries
from csvs import CSVs
from yadisk_connect import YaDisk
import logging


class Vacancies:
    name_of_fields = ['id', 'name', 'area', 'salary', 'address', 'response_url', 'published_at', 'created_at',
                      'archived', 'apply_alternate_url', 'alternate_url', 'employer', 'snippet', 'schedule',
                      'working_days', 'working_time_intervals', 'working_time_modes', 'accept_temporary']
    vacancies_array = {}
    currencies = {}
    number_of_vacancies, number_of_changes, every_day_checks_counter, every_hour_checks_counter, count_duplicates = \
        [0 for _ in range(5)]
    json_urls = []
    errors = 0

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
            logging.info(f"{params['date_from'][:10]} founded {str(vacancies['found'])} vacancies")
            self.every_day_checks_counter += vacancies['found']
            Dirs.make_dir('C:/Users/mi/work/hh_parser/vacancies/',
                          (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%d"))
            if vacancies['found'] > 2000:
                # self.separating_by_hours(query, params, today, days_ago)
                self.separating_by_hours_with_threads(query, today, days_ago)
            else:
                self.check_pages(query, params)
                self.number_of_changes += (len(list(self.vacancies_array.keys())))
            date = (today - datetime.timedelta(days=days_ago + 1)).strftime("%Y-%m-%d")
            CSVs.write_in_csv(self.vacancies_array, date)
            CSVs.write_jsons_in_csv(self.json_urls, date)
            self.json_urls = []

    def separating_by_hours(self, query, params, today, days_ago):
        cur_day = today - datetime.timedelta(days=days_ago)
        self.query_between_hours(query, params, cur_day, 0, 4)
        for hour in range(4, 18):
            self.query_between_hours(query, params, cur_day, hour, hour+1)
        self.query_between_hours(query, params, cur_day, 18, 20)
        self.query_between_hours(query, params, cur_day, 20, 24)

    def query_between_hours(self, query, params, cur_day, date_to_hours, date_from_hours):
        params['date_to'] = (cur_day - datetime.timedelta(hours=date_to_hours)).strftime("%Y-%m-%dT%H:%M:%S")
        params['date_from'] = (cur_day - datetime.timedelta(hours=date_from_hours)).strftime("%Y-%m-%dT%H:%M:%S")
        params['page'] = None
        vacancies = APIHHConnect.connect(query, params)
        logging.info(f"From {params['date_from']} to {params['date_to']} founded {str(vacancies['found'])} vacancies")
        self.end_of_qbh(vacancies, query, params)

    def separating_by_hours_with_threads(self, query, today, days_ago):
        cur_day = today - datetime.timedelta(days=days_ago)
        for hour in range(0, 24, 4):
            self.threads(query, cur_day, hour)

    def threads(self, query,  cur_day, hour):
        threads = []
        for x in range(4):
            params = {'specialization': '1', 'per_page': 100,
                      'date_from': (cur_day - datetime.timedelta(hours=hour + x + 1)).strftime("%Y-%m-%dT%H:%M:%S"),
                      'date_to': (cur_day - datetime.timedelta(hours=hour + x)).strftime("%Y-%m-%dT%H:%M:%S")}
            t = threading.Thread(target=self.query_between_hours_with_threads, args=(query, params))
            threads.append(t)
            t.start()
            params = {}
        for t in threads:
            t.join()

    def query_between_hours_with_threads(self, query, params):
        vacancies = APIHHConnect.connect(query, params)
        logging.info(f"From {params['date_from']} to {params['date_to']} founded {str(vacancies['found'])} vacancies")
        self.end_of_qbh(vacancies, query, params)

    def end_of_qbh(self, vacancies, query, params):
        self.every_hour_checks_counter += vacancies['found']
        if vacancies['found'] > 2000:
            logging.error(f"From {params['date_from']} to {params['date_to']} founded more than 2000 vacancies!")
        cur_len = len(list(self.vacancies_array.keys()))
        self.check_pages(query, params)
        self.number_of_changes += (len(self.vacancies_array) - cur_len)

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
            self.number_of_vacancies += 1
            if vacancy['archived']:
                continue
            vacancy_to_add = Vacancy.create_vacancy(vacancy, self.currencies)
            self.vacancies_array[vacancy_to_add.vacancy_id] = vacancy_to_add
            if CSVs.check_csv(vacancy_to_add):
                self.json_urls.append([vacancy_to_add.vacancy_id, vacancy_to_add.url_json])
                CSVs.create_csv(vacancy_to_add)
            else:
                if not CSVs.check_csv(vacancy_to_add):
                    self.count_duplicates += 1

    def start(self):
        """
        :return: запуск приложения
        """
        number_of_days = 30
        logging.basicConfig(level=logging.INFO,
                            filename=f"/vacancies_logs/vacancies_log{datetime.datetime.today().strftime('%Y-%m-%dT%H--%M--%S')}.log",
                            filemode="w", format="%(asctime)s %(levelname)s %(message)s")
        logging.info(f"Checking of last {number_of_days} days started.")
        # self.currencies = ParametersForQueries.get_currencies()
        # self.check_all(number_of_days)
        # YaDisk.write_on_yadisk()
        # logging.info(self.every_day_checks_counter)
        # logging.info(self.every_hour_checks_counter)
        # logging.info(self.count_duplicates)
        # self.upload_all_jsons()
        # print(self.errors)


start = pc()
Vacancies().start()
logging.info(f"Program works {round(pc() - start)} seconds")
