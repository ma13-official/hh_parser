import json
from api_hh_connect import APIHHConnect


class ParametersForQueries:
    @staticmethod
    def get_and_print_sorted(query):
        """
        !!!Функция изначально создавалась для парсинга JSON по ссылке "https://api.hh.ru/specializations".!!!

        JSON по ссылке "https://api.hh.ru/specializations" имеет следующую структуру:
            - массив словарей(один словарь - одна область специализаций);
            - каждый такой словарь имеет три поля:
                - id;
                - name;
                - specializations (массив специализаций).
        Реализованная функция:
            - делает запрос, получает JSON;
            - парсит JSON в массив с подобной структурой;
            - сортирует массив по id областей специализаций и массив специализаций по их id;
            - выводит полученный результат.
        :param query: страница для парсинга и вывода, поддерживаются "specializations" и "industries".
        :return: красиво выводит отсортированную структуру JSON-файла.
        """
        def get_data(x):
            """
            :param x: словарь в котором необходимо выбрать ключ для сортировки;
            :return: если число (x["id"]) имеет дробную часть - int-значение дробной части числа,
                     иначе - само число
            """
            x = x["id"]
            copy_x = x
            for i in x:
                x = x[1:]
                if i == ".":
                    break
            else:
                x = copy_x
            return int(x)

        specializations = APIHHConnect.connect(query)
        for spec in specializations:
            spec[query] = sorted(spec[query], key=get_data)
        specializations = sorted(specializations, key=get_data)
        for group in specializations:
            print("----------------------------------------")
            print(group["id"], group["name"])
            print("----------------------------------------")
            for item in group[query]:
                print("    ", item["id"], item["name"])

    @staticmethod
    def get_and_print_like_json(query):
        """
        :param query: страница для вывода.
        :return: выводит JSON в красивом формате.
        """
        data = APIHHConnect.connect(query)
        print(json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))


ParametersForQueries.get_and_print_sorted("specializations")
