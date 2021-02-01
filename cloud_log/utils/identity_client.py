# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache

from identity_client.client import Client as identity_client


BASE_URL = settings.IDENTITY_BASE_URL
AUTH_USERNAME = settings.SERVICE_AUTH_USERNAME
AUTH_PASSWORD = settings.SERVICE_AUTH_PASSWORD
USER_TYPE = 'service'


class IdentityClient(object):
    version = 'v1.0.0'

    def __init__(self, user_type='service'):
        self.identity_client = self.get_identity_client(user_type)

    @staticmethod
    def get_identity_client(user_type):
        return identity_client(auth_url=BASE_URL, username=AUTH_USERNAME, password=AUTH_PASSWORD,
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
        """
        平台侧获取云环境中所有分配出去的资源
        :return:
        """
        return self.identity_client.vdc.assigned(cloud_env_id, resource_type)