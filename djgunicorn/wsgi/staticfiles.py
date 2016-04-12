"""WSGI config for Gunicorn with staticfiles enabled.

This module is designed not to be imported directly, but provided to be
loaded by Gunicorn when it is launched.
"""

from django.contrib.staticfiles.handlers import StaticFilesHandler
from .base import application

application = StaticFilesHandler(application)
