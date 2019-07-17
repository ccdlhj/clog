# -*- coding: utf-8 -*-


class ClogAuthTokenMiddleware(object):

    def pre_call(self, context, action):
        # TODO：通过api验证token
        pass

    def post_call(self, context, action, result):
        pass