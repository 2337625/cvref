# -*- coding: utf-8 -*-
from webtemplate.settings import PROJECT_ROOT
from .base import *
from .app import *

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

try:
    from local import *
except ImportError:
    raise Exception('Create local.py from sample_local.py')

