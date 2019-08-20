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

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUGER = True

if DEBUG and DEBUGER:
    INSTALLED_APPS.append('debug_toolbar')

    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False
    }

    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    try:
        # Remove middlware cache.
        MIDDLEWARE_CLASSES.remove(
            'django.middleware.cache.UpdateCacheMiddleware')
        MIDDLEWARE_CLASSES.remove(
            'django.middleware.cache.FetchFromCacheMiddleware')
    except ValueError:
        pass

try:
    from local import *
except ImportError:
    raise Exception('Create local.py from sample_local.py')

