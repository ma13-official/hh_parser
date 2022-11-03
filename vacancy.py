from openpyxl.workbook import Workbook


class Vacancy:
    def __init__(self, vacancy_id, name, area, address, employer, url,
                 salary_from=None, salary_to=None, requirement=None, responsibility=None):
        self.vacancy_id = vacancy_id
        self.name = name
        self.area = area
        self.address = address
        self.employer = employer
        self.url = url + ' '
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.requirement = requirement
        self.responsibility = responsibility
        self.create_csv()

    def create_csv(self):
        wb = Workbook()
        ws = wb.active
        names_of_fields = ['id', 'name', 'area', 'address', 'employer', 'url',
                           'salary_from', 'salary_to', 'requirement', 'responsibility']
        ws.append(names_of_fields)
        fields = [self.vacancy_id, self.name, self.area, self.address, self.employer, self.url,
                  self.salary_from, self.salary_to, self.requirement, self.responsibility]
        ws.append(fields)
        wb.save('./vacancies/' + str(self.vacancy_id) + '.csv')
