""" 
    Author: Andrija Gajic 0033-2021
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'MIRROR': 'default',
        }
    }
}