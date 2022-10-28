import operator

import requests
from openpyxl import Workbook


class APIHHConnect:
    def __init__(self):
        self.specializations = None
        self.vacancies = None
        self.vacancies_array = []
        self.cur_number = 0

    def checking_all_pages(self):
        for x in range(0, 20, 1):
            self.get_vacancies(x)
            self.filling_vacancies_array(self.vacancies)

    def get_vacancies(self, page):
        url = "https://api.hh.ru/vacancies"
        params = {'per_page': 100, 'page': page}
        self.vacancies = requests.get(url, params).json()

    """
        JSON по ссылке "https://api.hh.ru/specializations" имеет следующую структуру:
            - массив словарей(один словарь - одна область специализаций);
            - каждый такой словарь имеет три поля:
                - id:
                - name;
                - specializations (массив специализаций).
        Реализованная функция:
            - делает запрос, получает JSON;
            - парсит JSON в массив с подобной структурой;
            - сортирует массив по id областей специализаций и массив специализаций по их id;
            - выводит полученный результат.
        """
    def get_specializations(self):
        url = "https://api.hh.ru/specializations"
        self.specializations = requests.get(url).json()
        specializations_parsed = []
        for group in self.specializations:
            specs = {"id": int(group["id"]),
                     "name": group["name"],
                     "specializations": []}
            for spec in group["specializations"]:
                specs["specializations"].append({"id": spec["id"],
                                                 "name": spec["name"]})
            specs["specializations"] = sorted(specs["specializations"], key=self.get_data)
            specializations_parsed.append(specs)
        specializations_parsed = sorted(specializations_parsed, key=operator.itemgetter("id")).copy()
        for group in specializations_parsed:
            print("----------------------------------------")
            print(group["id"], group["name"])
            print("----------------------------------------")
            for item in group["specializations"]:
                print("    ", item["id"], item["name"])
        # print(json.dumps(self.specializations, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))

    @staticmethod
    def get_data(x):
        x = x["id"]
        for i in x:
            x = x[1:]
            if i == ".":
                break
        return int(x)

    def filling_vacancies_array(self, vacancies):
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            self.cur_number += 1
            cur_vacancy = [self.cur_number]
            for field in list(vacancy.keys()):
                cur_vacancy.append(self.check_inner_fields(vacancy, field))
            self.vacancies_array.append(cur_vacancy)

    @staticmethod
    def check_inner_fields(vacancy, field):
        if vacancy[field] is not None:
            if isinstance(vacancy[field], dict):
                if len(vacancy[field]) == 2 or field == 'area' or field == 'employer':
                    if field != 'snippet':
                        return vacancy[field]['name']
                    else:
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


APIHHConnect().start()
