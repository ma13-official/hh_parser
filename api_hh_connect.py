import json

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
        if list(data.keys())[0] == 'errors':
            if data['errors'][0]['value'] == 'captcha_required':
                print(data['errors'][0]['captcha_url'] + '&backurl=' + query)
                with open(
                        f"C:/Users/mi/OneDrive - ITMO UNIVERSITY/work/hh_parser/captcha_json{data['request_id']}.json",
                        'w', encoding='utf8') as outfile:
                    json.dump(data, outfile, sort_keys=False, indent=4, ensure_ascii=False,
                              separators=(',', ': '))
                x = input()
                APIHHConnect.connect(query, params)  # потенциальная ошибка, если backurl кидает не туда
            else:
                print(data)
        else:
            params['backurl'] = None
        return data
