"""WSGI config for Gunicorn with staticfiles enabled.

This module is designed not to be imported directly, but provided to be
loaded by Gunicorn when it is launched.
"""

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.servers.basehttp import get_internal_wsgi_application

application = StaticFilesHandler(get_internal_wsgi_application())
