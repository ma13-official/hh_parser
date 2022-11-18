import schedule
import time
from vacancies import Vacancies

schedule.every().day.at("02:00").do(Vacancies.start)

while 1:
    schedule.run_pending()
    time.sleep(1)
