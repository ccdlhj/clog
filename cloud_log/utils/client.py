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
    base_url = settings.API_BASE_URL
    version = 'v1.0.0'

    def __init__(self, version='v1.0.0'):
        self.version = version

    def list(self, data=None):
        url = self.base_url + 'api/' + self.version + '/clog/collect'
        r = requests.post(url, data=data)
        clogs = []
        for i in r.json().get('data', []):
            clogs.append(ClogResouce(**i))
        return clogs

    def condition_list(self, data=None):
        url = self.base_url + 'api/' + self.version + '/clog/conditionList/collect'
        r = requests.post(url, data=data)
        clogs = []
        for i in r.json().get('data', []):
            clogs.append(ClogResouce(**i))
        return clogs

    def create(self, data=None):
        url = self.base_url + 'api/' + self.version + '/clog/spawn'
        r = requests.post(url, data=data)
        clog = ClogResouce(**r.json().get('data'))
        return clog

    def get(self, clog_id):
        url = self.base_url + 'api/' + self.version + '/clog/' + clog_id + '/show'
        r = requests.get(url)
        clog = ClogResouce(**r.json().get('data'))
        return clog

    def update(self, clog_id, data=None):
        url = self.base_url + 'api/' + self.version + '/clog/' + clog_id + '/modify'
        r = requests.post(url, data=data)
        if r.status_code == 200:
            return True
        else:
            return False


if __name__ == '__main__':
    data = {
        'res_org_id': 'abc',
        'created_at': '2021-09-21 11:11:11'
    }
    client = ClogClient()
    clog = client.update('1', data)
    print clog
