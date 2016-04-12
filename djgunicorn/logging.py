import functools
import os
import time
import traceback

import gunicorn.glogging

from django.core.management.color import color_style


def colorize(style, msg, resp):
    """Taken and modified from `django.utils.log.ServerFormatter.format`
    to mimic runserver's styling.
    """
    code = resp.status.split(maxsplit=1)[0]
    if code[0] == '2':
        # Put 2XX first, since it should be the common case
        msg = style.HTTP_SUCCESS(msg)
    elif code[0] == '1':
        msg = style.HTTP_INFO(msg)
    elif code == '304':
        msg = style.HTTP_NOT_MODIFIED(msg)
    elif code[0] == '3':
        msg = style.HTTP_REDIRECT(msg)
    elif code == '404':
        msg = style.HTTP_NOT_FOUND(msg)
    elif code[0] == '4':
        msg = style.HTTP_BAD_REQUEST(msg)
    else:
        # Any 5XX, or any other response
        msg = style.HTTP_SERVER_ERROR(msg)
    return msg


class GunicornLogger(gunicorn.glogging.Logger):
    """Custom logger class to add styling to access logs.

    Note that this is not a `logging.Logger` instance.
    """
    datefmt = r'[%d/%b/%Y %H:%M:%S]'    # Same date format as runserver.

    def __init__(self, cfg):
        super(GunicornLogger, self).__init__(cfg)
        if os.environ.get('DJANGO_COLORS') == 'nocolor':
            self.stylize = lambda msg, resp: msg
        else:
            self.stylize = functools.partial(colorize, color_style())

    def now(self):
        """Override to return date in runserver's format.
        """
        return time.strftime(r'[%d/%b/%Y:%H:%M:%S]')

    def make_access_message(self, resp, req, environ, request_time):
        safe_atoms = self.atoms_wrapper_class(
            self.atoms(resp, req, environ, request_time),
        )
        return self.stylize(self.cfg.access_log_format % safe_atoms, resp)

    def access(self, resp, req, environ, request_time):
        """Override to apply styling on access logs.

        This duplicates a large portion of `gunicorn.glogging.Logger.access`,
        only adding
        """
        if not (self.cfg.accesslog or self.cfg.logconfig or self.cfg.syslog):
            return

        msg = self.make_access_message(resp, req, environ, request_time)
        try:
            self.access_log.info(msg)
        except:
            self.error(traceback.format_exc())
