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
* Check depedency versions.
* Support for additional Gunicorn configs that may be useful. SSL seems to
  be a common need.
* Is it possible to conditionally replace the ``runserver`` command? By
  installing an alternative app config, for example?
