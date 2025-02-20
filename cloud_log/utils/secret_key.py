# -*- coding: utf-8 -*-

import os
import random
import string

from oslo_concurrency import lockutils


class FilePermissionError(Exception):
    """The key file permissions are insecure."""
    pass


def generate_key(key_length=64):
    """Secret key generator.

    The quality of randomness depends on operating system support,
    see http://docs.python.org/library/random.html#random.SystemRandom.
    """
    if hasattr(random, 'SystemRandom'):
        choice = random.SystemRandom().choice
    else:
        choice = random.choice
    return ''.join(map(lambda x: choice(string.digits + string.ascii_letters),
                   range(key_length)))


def generate_or_read_from_file(key_file='.secret_key', key_length=64):
    """Multiprocess-safe secret key file generator.

    Useful to replace the default (and thus unsafe) SECRET_KEY in settings.py
    upon first start. Save to use, i.e. when multiple Python interpreters
    serve the dashboard Django application (e.g. in a mod_wsgi + daemonized
    environment).  Also checks if file permissions are set correctly and
    throws an exception if not.
    """
    abspath = os.path.abspath(key_file)
    lock = lockutils.external_lock(key_file + ".lock",
                                   lock_path=os.path.dirname(abspath))
    with lock:
        if not os.path.exists(key_file):
            key = generate_key(key_length)
            old_umask = os.umask(0o177)  # Use '0600' file permissions
            with open(key_file, 'w') as f:
                f.write(key)
            os.umask(old_umask)
        else:
            if (os.stat(key_file).st_mode & 0o777) != 0o600:
                raise FilePermissionError("Insecure key file permissions!")
            with open(key_file, 'r') as f:
                key = f.readline()
        return key
