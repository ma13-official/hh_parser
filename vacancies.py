from api_hh_connect import APIHHConnect
from openpyxl import Workbook


class Vacancies:
    name_of_fields = ['id', 'name', 'area', 'salary', 'address', 'response_url', 'published_at', 'created_at',
                      'archived', 'apply_alternate_url', 'alternate_url', 'employer', 'snippet', 'schedule',
                      'working_days', 'working_time_intervals', 'working_time_modes', 'accept_temporary']
    vacancies_array = []
    number_of_vacancies = 0

    def checking_all_pages(self,
                           text=None,
                           area=None,
                           metro=None,
                           specialization=None,
                           industry=None,
                           employer_id=None,
                           currency=None,
                           salary=None):
        """
        :param text: параметры запроса
        :param area:
        :param metro:
        :param specialization:
        :param industry:
        :param employer_id:
        :param currency:
        :param salary:
        :return: выполнение 20 запросов, запись вакансий в двумерный массив.
        """
        value = 'vacancies'
        params = {'text': text,
                  'area': area,
                  'metro': metro,
                  'specialization': specialization,
                  'industry': industry,
                  'employer_id': employer_id,
                  'currency': currency,
                  'salary': salary,
                  'per_page': 100}
        for x in range(0, 20, 1):
            params['page'] = 0
            vacancies = APIHHConnect.connect(value, params)
            # self.filling_vacancies_array(vacancies)
            self.get_needed_fields(vacancies)

    def get_needed_fields(self, vacancies):
        """
        :param vacancies: JSON-объект полученный после запроса
        :return: заполнение двумерного массива vacancies_array необходимыми полями.
        """
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            self.number_of_vacancies += 1
            cur_vacancy = [self.number_of_vacancies]
            if vacancy['archived']:
                continue
            for field in self.name_of_fields:
                cur_vacancy.append(self.check_inner1(vacancy, field))
            self.vacancies_array.append(cur_vacancy)

    def filling_vacancies_array(self, vacancies):
        """
        :param vacancies: JSON-объект полученный после запроса
        :return: заполнение двумерного массива vacancies_array необходимыми полями.
        """
        for vacancy in vacancies[list(vacancies.keys())[0]]:
            self.number_of_vacancies += 1
            cur_vacancy = [self.number_of_vacancies]
            for field in list(vacancy.keys()):
                cur_vacancy.append(self.check_inner2(vacancy, field))
            self.vacancies_array.append(cur_vacancy)

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

    @staticmethod
    def check_inner2(vacancy, field):
        """
        :param vacancy: вакансия - одна из ста полученных в JSON-объекта;
        :param field: поле вакансии, которое необходимо рассмотреть;
        :return: общее значение для добавления в двумерный массив.
        """
        if vacancy[field] is not None:
            if isinstance(vacancy[field], dict):
                if len(vacancy[field]) == 2 or field == 'area' or field == 'employer':
                    if field != 'snippet' and field != 'insider_interview':
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
                return str(vacancy[field]['from']) + ' - ' + str(vacancy[field]['to'])
            else:
                if not vacancy[field]:
                    return None
                return vacancy[field]

    def write_in_xlsx(self):
        """
        :return: запись двумерного массива в Excel-таблицу.
        """
        wb = Workbook()
        ws = wb.active
        ws.append(self.name_of_fields)
        for item in self.vacancies_array:
            ws.append(item)
        wb.save('vacancies.xlsx')

    def start(self,
              text=None,
              area=None,
              metro=None,
              specialization=None,
              industry=None,
              employer_id=None,
              currency=None,
              salary=None):
        """
        :param text:
        :param area:
        :param metro:
        :param specialization:
        :param industry:
        :param employer_id:
        :param currency:
        :param salary:
        :return: запуск приложения
        """
        self.checking_all_pages(text, area, metro, specialization, industry, employer_id, currency, salary)
        self.write_in_xlsx()


Vacancies().start()
