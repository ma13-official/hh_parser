import requests


class APIHHConnect:
    @staticmethod
    def connect(query, params={}):
        url = "https://api.hh.ru/" + query
        data = requests.get(url, params).json()
        if list(data.keys())[0] == 'errors':
            if data['errors'][0]['value'] == 'captcha_required':
                print(params)
                params['backurl'] = data['errors'][0]['captcha_url'] + '&backurl=' + query
                APIHHConnect.connect(query, params)  # потенциальная ошибка, если backurl кидает не туда
            else:
                print(data)
        else:
            params['backurl'] = None
        return data
