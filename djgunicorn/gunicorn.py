import subprocess

from django.conf import settings


def build_gunicorn_arguments(addr, port, options):
    handle_static_files = (
        options['use_static_handler'] and
        (settings.DEBUG or options['insecure_serving'])
    )
    app_name = 'static_handler' if handle_static_files else 'django_handler'
    args = [
        'djgunicorn.wsgi:' + app_name,
        '--bind', '{addr}:{port}'.format(addr=addr, port=int(port)),
        '--access-logfile', '-',
        '--access-logformat', '%(t)s "%(r)s" %(s)s %(B)s',
        '--error-logfile', '-',
        '--log-level', 'warning',
    ]
    if options['use_reloader']:
        args.append('--reload')
    return args


class GunicornRunner(object):

    gunicorn = 'gunicorn'

    def __init__(self, args):
        args = [self.gunicorn] + args
        self.proc = subprocess.Popen(args, universal_newlines=True)

    def run(self):
        self.proc.wait()


def run(addr, port, options, ipv6=False, threading=False):
    """Patched runserver internal with Gunicorn.
    """
    args = build_gunicorn_arguments(addr=addr, port=port, options=options)
    runner = GunicornRunner(args)
    runner.run()
