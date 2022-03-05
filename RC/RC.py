import hashlib
import requests
import json


class RC:
    def __init__(self, private_key, public_key):
        self.priv_key = private_key
        self.pub_key = public_key

    def _string_for_hash(self, params: dict):
        sort_key = sorted(params.keys())
        string_for_hash = ''
        for k in sort_key:
            if isinstance(params[k], dict):
                string_for_hash += '{key}='.format(key=k) + self._string_for_hash(params[k])
            else:
                string_for_hash += '{key}={value}'.format(key=k, value=params[k])
        return string_for_hash

    def _sign(self, params: dict) -> str:
        return hashlib.md5((self._string_for_hash(params) + self.priv_key).encode('UTF-8')).hexdigest()

    def get_bookings(self, begin_date, end_date, **kwargs):
        url = 'https://realtycalendar.ru/api/v1/bookings/' + self.pub_key
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        params = {
            'begin_date': begin_date,
            'end_date': end_date
        }

        params['sign'] = self._sign(params)

        answer = requests.post(url, json.dumps(params), headers=headers)

        return answer.json()

