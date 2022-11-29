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
            case 'id':
                return vacancy[field]
            case 'name':
                return vacancy[field]
            case 'area':
                return vacancy[field]['id']
            case 'salary':
                return str(vacancy[field]['from']) + ' - ' + str(vacancy[field]['to'])
            case 'address':
                return vacancy[field]['raw']
            case 'response_url':
                return vacancy[field]
            case 'published_at':
                return vacancy[field]
            case 'created_at':
                return vacancy[field]
            case 'archived':
                return vacancy[field]
            case 'apply_alternate_url':
                return vacancy[field]
            case 'alternate_url':
                return vacancy[field]
            case 'employer':
                return vacancy[field]['name']
            case 'snippet':
                return str(vacancy[field]['requirement']) + '\n' + str(vacancy[field]['responsibility'])
            case 'schedule':
                return vacancy[field]['id']
            case 'working_days':
                return vacancy[field][0]['id']
            case 'working_time_intervals':
                return vacancy[field][0]['id']
            case 'working_time_modes':
                return vacancy[field][0]['id']
            case 'accept_temporary':
                return vacancy[field]

    def separating_by_hours(self, query, params, today, days_ago):
        cur_day = today - datetime.timedelta(days=days_ago)
        self.query_between_hours(query, params, cur_day, 0, 4)
        for hour in range(4, 18):
            self.query_between_hours(query, params, cur_day, hour, hour + 1)
        self.query_between_hours(query, params, cur_day, 18, 20)
        self.query_between_hours(query, params, cur_day, 20, 24)

    def query_between_hours(self, query, params, cur_day, date_to_hours, date_from_hours):
        params['date_to'] = (cur_day - datetime.timedelta(hours=date_to_hours)).strftime("%Y-%m-%dT%H:%M:%S")
        params['date_from'] = (cur_day - datetime.timedelta(hours=date_from_hours)).strftime("%Y-%m-%dT%H:%M:%S")
        params['page'] = None
        vacancies = APIHHConnect.connect(query, params)
        logging.info(f"From {params['date_from']} to {params['date_to']} founded {str(vacancies['found'])} vacancies")
        self.end_of_qbh(vacancies, query, params)