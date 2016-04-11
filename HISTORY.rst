History
-------

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
