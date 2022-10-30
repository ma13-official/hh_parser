import requests


class APIHHConnect:
    @staticmethod
    def connect(query, params=None):
        url = "https://api.hh.ru/" + query
        data = requests.get(url, params).json()
        return data
