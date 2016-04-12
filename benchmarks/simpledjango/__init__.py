"""An ultra-minimal Django setup that we'll use for benchmarking.

To run::

    python simpledjango/manage.py runserver

<http://softwaremaniacs.org/blog/2011/01/07/django-micro-framework/en/>
"""

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse


def page(request):
    return HttpResponse('It works!')


urlpatterns = [
    url(r'^$', page),
]


application = get_wsgi_application()
