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