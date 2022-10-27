import requests
from openpyxl import Workbook


class api_hh_connect:
    def __init__(self):
        self.vacancies = None
        self.vacancies_array = []
        self.cur_number = 0

    def checking_all_pages(self):
        for x in range(0, 20, 1):
            self.creating_connection(x)
            self.filling_vacancies_array(self.vacancies)

    def creating_connection(self, page):
        url = "https://api.hh.ru/vacancies"
        params = {'per_page': 100, 'page': page}
        self.vacancies = requests.get(url, params).json()

    def filling_vacancies_array(self, vacancies):
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            self.cur_number += 1
            cur_vacancy = [self.cur_number]
            try:
                for field in list(vacancy.keys()):
                    cur_vacancy.append(self.check_inner_fields(vacancy, field))
            except:
                print(vacancies.keys())
            self.vacancies_array.append(cur_vacancy)

    @staticmethod
    def check_inner_fields(vacancy, field):
        if vacancy[field] is not None:
            if isinstance(vacancy[field], dict):
                if len(vacancy[field]) == 2 or field == 'area' or field == 'employer':
                    try:
                        return vacancy[field]['name']
                    except:
                        return None
            if isinstance(vacancy[field], list):
                if not vacancy[field]:
                    return None
                return vacancy[field][0]['name']
            if field == 'address':
                return vacancy[field]['raw']
            elif field == 'salary':
                return str(vacancy[field]['from']) + '-' + str(vacancy[field]['to'])
            else:
                if not vacancy[field]:
                    return None
                return vacancy[field]

    def write_in_xlsx(self):
        wb = Workbook()
        ws = wb.active
        name_of_fields = ['number'] + list(self.vacancies['items'][0].keys())
        ws.append(name_of_fields)
        for item in self.vacancies_array:
            ws.append(item)
        wb.save('123.xlsx')

    def start(self):
        self.checking_all_pages()
        self.write_in_xlsx()


api_hh_connect().start()