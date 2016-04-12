"""Gunicorn configuration file used by gunserver's Gunicorn subprocess.

This module is not designed to be imported directly, but provided as
Gunicorn's configuration file.
"""

import os
import sys

import django
import gunicorn


# General configs.
bind = os.environ['DJANGO_ADDRPORT']
logger_class = 'djgunicorn.logging.GunicornLogger'


def post_worker_init(worker):
    """Hook into Gunicorn to display message after launching.

    This mimics the behaviour of Django's stock runserver command.
    """
    quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
    sys.stdout.write(
        "Django version {djangover}, Gunicorn version {gunicornver}, "
        "using settings {settings!r}\n"
        "Starting development server at http://{addrport}/\n"
        "Quit the server with {quit_command}.\n".format(
            djangover=django.get_version(),
            gunicornver=gunicorn.__version__,
            settings=os.environ.get('DJANGO_SETTINGS_MODULE'),
            addrport=bind,
            quit_command=quit_command,
        ),
    )


def worker_exit(server, worker):
    """Hook into Gunicorn to display message after existing.

    The purpose of this hook is purely cosmetic: we want a newline after the
    worker reloads. This has an unintended side effect to display an extra
    newline after the server quits, but it is relatively unimportant.
    """
    sys.stdout.write('\n')
