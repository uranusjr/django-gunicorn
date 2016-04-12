import os
import sys

# Make sure we can access the simpledjango directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DEBUG = True

ROOT_URLCONF = 'simpledjango'

INSTALLED_APPS = ['djgunicorn']

SECRET_KEY = 'm05k7'

TIME_ZONE = 'UTC'
