# -*- coding:utf-8 -*-
import time

from functools import wraps


class StopRetry(Exception):
    """retry exception

        Default retry exception
    """

    def __repr__(self):
        return 'retry stop'


def retry(max_retry=1000, interval=5, exception=Exception):
    """
        retry exception
    """

    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            retry_count = max_retry
            retry_interval = interval
            while retry_count:
                start = time.time()
                try:
                    return func(*args, **kwargs)
                except exception:
                    retry_count -= 1
                    retry_interval = (time.time() - start) - retry_interval
                    if retry_interval < 0:
                        time.sleep(-retry_interval)
            else:
                raise StopRetry

        return _wrapper

    return wrapper
