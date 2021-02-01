import requests
from django.conf import settings
from django.core.cache import cache
from identity_client.client import Client as Identity_client

BASE_URL = settings.IDENTITY_BASE_URL
AUTH_USERNAME = settings.SERVICE_AUTH_USERNAME
AUTH_PASSWORD = settings.SERVICE_AUTH_PASSWORD
USER_TYPE = 'service'


class ClogResouce(object):
    id = ''

    def __init__(self, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __repr__(self):
        return '<clog>:{}'.format(str(self.id))


class ClogClient(object):
    version = 'v1.0.0'

    def __init__(self, version='v1.0.0', token=None, url=None):
        self.version = version
        self.token = 'Token ' + token
        self.base_url = url or settings.CLOG_API_BASE_URL

    def delete_null(self, data):
        params = dict()
        for key in data:
            if data.get(key) or key in ['Limit', 'Offset']:
                params[key] = data.get(key)
        return params

    def list(self, data=None):
        data = self.delete_null(data)
        url = self.base_url + 'api/' + self.version + '/clog/get_list'
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
        clogs_api_data = r.json().get('data', [])
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


class IdentityClient(object):
    version = 'v1.0.0'

    def __init__(self, user_type='service'):
        self.identity_client = self.get_identity_client(user_type)

    @staticmethod
    def get_identity_client(user_type):
        return Identity_client(auth_url=BASE_URL, username=AUTH_USERNAME, password=AUTH_PASSWORD,
                               user_type=user_type, cache=cache)

    def get_vdc_visible(self, res_org_id):
        return self.identity_client.vdc.service_list_visible(res_org_id=res_org_id, all=all)

    def get_vdc_show(self, res_org_id):
        return self.identity_client.vdc.service_get(res_org_id)

    def cloud_env_list(self, res_org_id=None):
        return self.identity_client.cloud_env.list_service(res_org_id)

    def cloud_env_show(self, cloud_env_id):
        return self.identity_client.cloud_env.get_service(cloud_env_id)

    def get_quotas(self, res_org_id, cloud_env_id):
        return self.identity_client.vdc.service_quota_list(res_org_id, cloud_env_id)

    def get_assigned_resource(self, res_org_id, cloud_env_id=None, resource_type=None):
        return self.identity_client.vdc.resources(res_org_id, cloud_env_id, resource_type)

    def update_in_use_quotas(self, res_org_id, cloud_env_id, data):
        return self.identity_client.vdc.service_quota_update(res_org_id, cloud_env_id, **data)

    def remove_association(self, resource_type, resource_id):
        return self.identity_client.vdc.remove_association(resource_id, resource_type)

    def get_project_path(self, res_org_uuid_list):
        return self.identity_client.vdc.service_path_list(res_org_uuid_list)

    def get_assigned_resource_all(self, cloud_env_id, resource_type):
        return self.identity_client.vdc.assigned(cloud_env_id, resource_type)
