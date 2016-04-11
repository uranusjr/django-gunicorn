import subprocess

from django.conf import settings


class GunicornRunner(object):

    executable = 'gunicorn'

    def __init__(self, addr, port, ipv6, options):
        args = self.build_arguments(addr, port, ipv6, options)
        self.proc = subprocess.Popen(args, universal_newlines=True)

    def build_arguments(self, addr, port, ipv6, options):
        handle_statics = (
            options['use_static_handler'] and
            (settings.DEBUG or options['insecure_serving'])
        )
        app_name = 'static_handler' if handle_statics else 'django_handler'
        addrport = (
            '[{addr}]:{port}' if ipv6
            else '{addr}:{port}'
        ).format(addr=addr, port=int(port))
        args = [
            self.executable,
            'djgunicorn.wsgi:' + app_name,
            '--bind', addrport,
            '--access-logfile', '-',
            '--access-logformat', '%(t)s "%(r)s" %(s)s %(B)s',
            '--error-logfile', '-',
            '--log-level', 'warning',
        ]
        if options['use_reloader']:
            args.append('--reload')
        return args

    def run(self):
        self.proc.wait()


def run(addr, port, options, ipv6=False, threading=False):
    """Patched runserver internal with Gunicorn.
    """
    runner = GunicornRunner(addr=addr, port=port, ipv6=ipv6, options=options)
    runner.run()
