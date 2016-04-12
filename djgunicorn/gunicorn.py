import os
import signal
import subprocess
import sys

from django.conf import settings


class GunicornRunner(object):

    executable = 'gunicorn'

    def __init__(self, addr, port, options):
        self.args = self.build_arguments(addr=addr, port=port, options=options)

    def build_arguments(self, addr, port, options):
        try:
            handle_statics = (
                options['use_static_handler'] and
                (settings.DEBUG or options['insecure_serving'])
            )
        except KeyError:
            handle_statics = False
        module = 'staticfiles' if handle_statics else 'base'

        # Change working directory to where manage.py is.
        working_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        args = [
            self.executable,
            'djgunicorn.wsgi.{module}:application'.format(module=module),
            '--bind', '{addr}:{port}'.format(addr=addr, port=int(port)),
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
        if settings.SETTINGS_MODULE:
            os.environ['DJANGO_SETTINGS_MODULE'] = settings.SETTINGS_MODULE
        self.proc = subprocess.Popen(self.args, universal_newlines=True)
        self.proc.wait()

    def shutdown(self):
        self.proc.send_signal(signal.SIGTERM)   # Graceful shutdown.


def run(addr, port, options):
    """Patched runserver internal with Gunicorn.
    """
    runner = GunicornRunner(addr=addr, port=port, options=options)
    runner.run()
    return runner
