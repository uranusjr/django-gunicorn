=============================
django-gunicorn
=============================

Run Django development server with Gunicorn.


Quickstart
----------

Install django-gunicorn::

    pip install djgunicorn

Then add it to your ``INSTALLED_APPS``. You will get a new command
``gunserver`` (please forgive my little pun-loving self). It runs like
Django's development server, but the HTTP handling is backed by Gunicorn.


Features
--------

You can find available options with::

    python manage.py help gunserver

Most options work as the built-in ``runserver`` command (in
``django.contrib.staticfiles``). Exceptions:

* The ``verbosity`` and ``no-color`` settings are *not* passed to Gunicorn.
  They still affect messages emitted by the command itself, however.
* The ``nothreading`` option does not do anything.


Todo
----

* Unit tests and CI.
* Check how low we can support Django and Gunicorn versions.
* Support for additional Gunicorn configs that may be useful. SSL seems to
  be a common need.
* Is it possible to conditionally replace the ``runserver`` command? By
  installing an alternative app config, for example?
* Output redirection. Currently we always use stderr, but we should respect
  ``Command.stdout`` and ``Command.stderr``.
* The startup message is not printed when reloading. It is possible to hook
  this with Gunicorn server hooks (through a config file), but the problem
  is how we can pass the correct information into it.


Interesting Links
-----------------

* `#21978 (Add optional gunicorn support to runserver) <https://code.djangoproject.com/ticket/21978>`_
* `Fixed #21978 -- Added optional gunicorn support to runserver. · django/django <https://github.com/django/django/pull/3461/files>`_
* `dj-static/dj_static.py · kennethreitz/dj-static <https://github.com/kennethreitz/dj-static/blob/485d626/dj_static.py>`_
* `SSL support for Django-admin runserver‏ <https://groups.google.com/forum/#!topic/django-developers/PgBcSEiUdw0/discussion>`_
