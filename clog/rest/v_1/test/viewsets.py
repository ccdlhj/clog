# -*- coding: utf-8 -*-

from t2cloud_rest import NoAuthViewSet, BaseViewSet
from t2cloud_rest import router, action


@router()
class TestNoAuthViewSet(NoAuthViewSet):

    @action(method='get')
    def test_no_auth(self, ids, query_params):
        return {'status': 'no auth'}


@router()
class TestAuthViewSet(BaseViewSet):

    @action(method='get')
    def test_auth(self, ids, query_params):
        return {'status': 'authed'}
