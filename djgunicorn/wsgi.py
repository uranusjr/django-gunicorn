from gunicorn.app.base import Application as BaseWSGIApplication

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.handlers.wsgi import WSGIHandler, get_path_info
from django.utils import six
from django.utils.six.moves.urllib.parse import urlparse


class WSGIApplication(BaseWSGIApplication):

    def __init__(self, options, handle_static_files):
        self.options = options
        handler = get_internal_wsgi_application()
        if handle_static_files:
            handler = StaticFilesWSGIHandler(handler)
        self.handler = handler
        super(WSGIApplication, self).__init__()

    def load_config(self):
        for key, value in six.iteritems(self.options):
            self.cfg.set(key, value)

    def load(self):
        return self.handler


def run(addr, port, options, ipv6=False, threading=False):
    """Patched runserver internal with Gunicorn.
    """
    handle_static_files = (
        options['use_static_handler'] and
        (settings.DEBUG or options['insecure_serving'])
    )
    wsgiapp = WSGIApplication(
        options={
            'bind': '{addr}:{port}'.format(addr=addr, port=int(port)),
            'reload': options['use_reloader'],
            'worker_class': 'sync',
        },
        handle_static_files=handle_static_files,
    )
    wsgiapp.run()


class StaticFilesWSGIHandler(WSGIHandler):
    """WSGI middleware that intercept static file access before Gunicorn.

    This handler is used to mimic the behaviour of
    `django.contrib.staticfiles.runserver`.

    This class is basically a stripped-down version of Cling by Kenneth Reitz
    that does not support old Django versions, and always uses the stock
    static file handler.
    """
    def __init__(self, django_handler):
        self.django_handler = django_handler
        self.base_url = urlparse(settings.STATIC_URL)
        self.handle = StaticFilesHandler(django_handler)
        super(StaticFilesWSGIHandler, self).__init__()

    def __call__(self, environ, start_response):
        # Hand non-static requests to Django.
        try:
            if not self._should_handle(get_path_info(environ)):
                return self.django_handler(environ, start_response)
        except UnicodeDecodeError:
            # Apparently a malformed URL. Just hand it to Django
            # for it to respond as it sees fit.
            return self.django_handler(environ, start_response)

        # Handle static requests.
        return self.handle(environ, start_response)

    def _should_handle(self, path):
        """Checks if the path should be handled. Ignores the path if:

        * the host is provided as part of the base_url
        * the request's path isn't under the media path (or equal)
        """
        return path.startswith(self.base_url[2]) and not self.base_url[1]
