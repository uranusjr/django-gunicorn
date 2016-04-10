=============================
django-gunicorn
=============================

Run Django development server with Gunicorn.


Quickstart
----------

Install django-gunicorn::

    pip install djgunicorn

Then add it to your ``INSTALLED_APPS``. You will get a new command
``gunserver`` (please forgive my little pun-loving self). This command
runs like Django's development server, but the HTTP handling is backed by
Gunnicorn.


Features
--------

You can find available options with::

    python manage.py help gunserver

Most options work as the built-in ``runserver`` command (in
``django.contrib.staticfiles``). Exceptions:

* The `verbosity` and `no-color` settings are *not* passed to Gunicorn. They
  will still affect messages emitted by the command itself, however.
* The `nothreading` option does not do anything.


Todo
----

* Unit tests and CI.
* Check depedency versions.

