#!/usr/bin/env python
# -*- coding: utf-8 -*-

import djgunicorn

from setuptools import setup, find_packages

version = djgunicorn.__version__

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

with open('requirements/base.txt') as f:
    install_requires = f.read().strip().splitlines()

setup(
    name='djgunicorn',
    version=version,
    description="""Run Django development server with Gunicorn.""",
    long_description=readme + '\n\n' + history,
    author='Tzu-ping Chung',
    author_email='uranusjr@gmail.com',
    url='https://github.com/uranusjr/django-gunicorn',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    license='BSD',
    zip_safe=False,
    keywords='django-gunicorn',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
