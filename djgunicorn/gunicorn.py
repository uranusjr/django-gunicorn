import os
import subprocess
import sys

from django.conf import settings


class GunicornRunner(object):

    executable = 'gunicorn'

    def __init__(self, addr, port, addr_display, options):
        self.addrport = '{addr_display}:{port}'.format(
            addr_display=addr_display,
            port=int(port),
        )
        self.args = self.build_arguments(options)

    def build_arguments(self, options):
        handle_statics = (
            options['use_static_handler'] and
            (settings.DEBUG or options['insecure_serving'])
        )
        app_name = 'static_handler' if handle_statics else 'django_handler'

        # Change working directory to where manage.py is.
        working_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        args = [
            self.executable,
            'djgunicorn.wsgi:' + app_name,
            '--config', 'python:djgunicorn.config',
            '--access-logfile', '-',
            '--access-logformat', '%(t)s "%(r)s" %(s)s %(B)s',
            '--error-logfile', '-',
            '--log-level', 'warning',
            '--chdir', working_dir,
        ]
        if options['use_reloader']:
            args.append('--reload')
        return args

    def run(self):
        # Pass information into the Gunicorn process through environ.
        # This seems to be how Django's stock runserver do things as well;
        # see `django.core.management.commands.runserver.Command.execute`.
        os.environ.update({
            'DJANGO_SETTINGS_MODULE': settings.SETTINGS_MODULE,
            'DJANGO_ADDRPORT': self.addrport,
        })
        proc = subprocess.Popen(
            self.args,
            universal_newlines=True,
        )
        proc.wait()


def run(addr, port, options, addr_display):
    """Patched runserver internal with Gunicorn.
    """
    runner = GunicornRunner(
        addr=addr, port=port, addr_display=addr_display,
        options=options,
    )
    runner.run()
