"""WSGI config for Gunicorn.

This module is designed not to be imported directly, but provided to be
loaded by Gunicorn when it is launched.
"""

from django.core.servers.basehttp import get_internal_wsgi_application

application = get_internal_wsgi_application()
