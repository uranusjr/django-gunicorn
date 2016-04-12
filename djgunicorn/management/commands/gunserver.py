from __future__ import print_function

import datetime
import importlib
import sys

from django.core.management import get_commands
from django.utils import six
from django.utils.encoding import get_system_encoding

from djgunicorn.gunicorn import run


# Use the active runserver command as base. This is generally provided by
# staticfiles, but can be django.core if it's not installed, or even something
# else if some third-party app overrides it.
def get_command_class(name):
    module = importlib.import_module('{app}.management.commands.{name}'.format(
        app=get_commands()[name], name=name,
    ))
    return module.Command

BaseCommand = get_command_class('runserver')


class Command(BaseCommand):

    help = "Starts a lightweight Web server for development with Gunicorn."

    def get_version(self):
        import djgunicorn
        return djgunicorn.__version__

    def run(self, **options):
        """Override runserver's entry point to bring Gunicorn on.

        A large portion of code in this method is copied from
        `django.core.management.commands.runserver`.
        """
        shutdown_message = options.get('shutdown_message', '')

        self.stdout.write("Performing system checks...\n\n")
        self.check(display_num_errors=True)
        self.check_migrations()
        now = datetime.datetime.now().strftime(r'%B %d, %Y - %X')
        if six.PY2:
            now = now.decode(get_system_encoding())
        self.stdout.write(now)

        addr, port = self.addr, self.port
        addr_display = '[{}]'.format(addr) if self._raw_ipv6 else addr

        try:
            run(addr, port, options, addr_display)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)
