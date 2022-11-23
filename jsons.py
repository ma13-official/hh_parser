import csv
import json
import os

from openpyxl import Workbook, load_workbook
from time import perf_counter as pc
from api_hh_connect import APIHHConnect
from dirs import Dirs


class JSONs:
    @staticmethod
    def save_vacancies_json(vacancies, params):
        path = r"C:/Users/mi/work/hh_parser/group_jsons/"
        name = f"{params['date_from'][:13]}---{params['page']}.json"
        if os.path.exists(path + name):
            return
        with open(path + name, 'w', encoding='utf8') as outfile:
            json.dump(vacancies, outfile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

    @staticmethod
    def upload_all_jsons():
        path = 'C:/Users/mi/OneDrive - ITMO UNIVERSITY/work/hh_parser/json_urls/'
        filename = '2022-11-18.xlsx'
        # for filename in os.listdir(path):
        cur = open(path + filename)
        directory = filename[:-4]
        Dirs.make_dir('C:/Users/mi/work/hh_parser/vacancies_jsons/', directory)
        file_reader = csv.DictReader(cur, delimiter=",")
        print(cur)
        count = 0
        start = pc()
        for row in file_reader:
            print(row)
            count += 1
            print(row['2'] + ' ' + str(count) + '   ' + str(pc() - start))
            JSONs.threads_upload_jsons(row['1'], directory)

    @staticmethod
    def threads_upload_jsons(url, directory):
        vacancy = APIHHConnect.connect(url)
        with open('C:/Users/mi/work/hh_parser/vacancies_jsons/' + directory + '/' + vacancy['id'] + '.json', 'w',
                  encoding='utf8') as outfile:
            try:
                json.dump(vacancy, outfile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
            except Exception as e:
                print(e)

    @staticmethod
    def get_json(v):
        PATH = 'C:/Users/mi/work/hh_parser/vacancies_jsons/'
        vacancy = APIHHConnect.connect('vacancies/' + v.vacancy_id)
        date = v.created_at[:10]
        os.chdir(PATH)
        if not os.path.isdir(date):
            os.mkdir(date)
        os.chdir(date)
        with open(PATH + date + '/' + str(v.vacancy_id) + '.json', 'w') as outfile:
            json.dump(vacancy, outfile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))