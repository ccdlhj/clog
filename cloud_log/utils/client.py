from django.conf import settings

import requests


class ClogResouce(object):
    id = ''

    def __init__(self, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __repr__(self):
        return '<clog>:{}'.format(str(self.id))


class ClogClient(object):
    base_url = settings.CLOG_API_BASE_URL
    version = 'v1.0.0'

    def __init__(self, version='v1.0.0', token=None):
        self.version = version
        self.token = 'Token ' + token

    def delete_null(self, data):
        params = dict()
        for key in data:
            if data.get(key) or key in ['Limit', 'Offset']:
                params[key] = data.get(key)
        return params

    def list(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/get_lst'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        clogs_api_data = r.json().get('data')
        clogs = []
        for i in clogs_api_data:
            clogs.append(ClogResouce(**i))
        return clogs

    def list_count(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/get_list_count'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        return r.json().get('data', {}).get('total', 0)

    def condition_list(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/conditionList/get_list'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        clogs_api_data = r.json().get('data',[])
        clogs = []
        for i in clogs_api_data:
            clogs.append(ClogResouce(**i))
        return clogs

    def condition_list_count(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/conditionList/get_list_count'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        return r.json().get('data', {}).get('total', 0)

    def create(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/spawn'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        clog = ClogResouce(**r.json().get('data'))
        return clog

    def get(self, clog_id):
        url = self.base_url + 'api/' + self.version + '/clog/' + clog_id + '/show'
        r = requests.get(url, headers={'Authorization': self.token})
        clog = ClogResouce(**r.json().get('data'))
        return clog

    def update(self, clog_id, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/' + clog_id + '/modify'
        r = requests.post(url, json=data, headers={'Authorization': self.token})
        if r.status_code == 200:
            return True
        else:
            return False