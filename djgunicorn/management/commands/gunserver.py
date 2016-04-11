from __future__ import print_function

from django.contrib.staticfiles.management.commands.runserver import (
    Command as BaseCommand,
)
from django.core.management.commands import runserver

from djgunicorn.gunicorn import run


class Command(BaseCommand):

    def get_version(self):
        import djgunicorn
        return djgunicorn.__version__

    def get_handler(self, *args, **options):
        """HACK: Pass information to Gunicorn.

        We don't use this handler, so it should be OK to reuse this. :p
        """
        return options

    def run(self, **options):
        """Always use inner_run directly. We'll handle autoreload in Gunicorn.
        """
        # HACK: Monkey-patch the built-in runserver internal to use Gunicorn.
        old_run, runserver.run = runserver.run, run
        self.inner_run(None, **options)
        runserver.run = old_run
