History
-------

0.3.0 (2016-04-13)
++++++++++++++++++

* Add Gunicorn config changing directory to where ``manage.py`` to avoid
  problems when ``manage.py`` is run in another directory.
* Info message is now displayed when Gunicorn reloads, as ``runserver`` does.
* Enable extended ``runserver`` provided by ``staticfiles`` only if it is
  installed (which is the default).
* Gunicorn access logs are now coloured, as ``runserver``'s.
* Get rid of a custom static handler in favour of Django's stock one.


0.2.0 (2016-04-12)
++++++++++++++++++

* Gunicorn invocation is re-implemented with ``subprocess`` to handle reloading
  gracefully. (`benoitc/gunicorn#935`_)


0.1.1 (2016-04-11)
++++++++++++++++++

* Lazy-load WSGI handler in Gunicorn application to avoid race conditions.


0.1.0 (2016-04-11)
++++++++++++++++++

* First release on PyPI.


.. _`benoitc/gunicorn#935`: <https://github.com/benoitc/gunicorn/issues/935>
