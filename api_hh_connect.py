import requests


class APIHHConnect:
    @staticmethod
    def connect(query, params=None):
        if params is None:
            params = {}
        if not query.startswith("https://api.hh.ru/"):
            url = "https://api.hh.ru/" + query
        else:
            url = query
        data = requests.get(url, params).json()
        try:
            if list(data.keys())[0] == 'errors':
                if data['errors'][0]['value'] == 'captcha_required':
                    print(params)
                    params['backurl'] = data['errors'][0]['captcha_url'] + '&backurl=' + query
                    APIHHConnect.connect(query, params)  # потенциальная ошибка, если backurl кидает не туда
                else:
                    print(data)
        except:
            print(url)
            print(data)
        else:
            params['backurl'] = None
        return data
