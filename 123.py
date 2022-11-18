import datetime
import json
import os
import csv

from api_hh_connect import APIHHConnect

# for filename in os.listdir('./123/'):
#     cur = open('./123/' + filename)
#     file_reader = csv.DictReader(cur, delimiter=",")
#     for row in file_reader:
#         print(row)
# vacancy = APIHHConnect.connect('vacancies/' + '50625586')
# with open('50625586.json', 'w') as outfile:
#     json.dump(vacancy, outfile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

# today = datetime.date.today()
# os.chdir('C:/Users/mi/work/hh_parser/vacancies/')
# for x in range(2, 100):
#     cur = (today - datetime.timedelta(days=x)).strftime("%Y-%m-%d")
#     os.mkdir(cur)
#     cur = (today + datetime.timedelta(days=x)).strftime("%Y-%m-%d")
#     os.mkdir(cur)
