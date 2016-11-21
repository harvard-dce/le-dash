from base import * # noqa
import logging

DEBUG = True

INTERNAL_IPS = INTERNAL_IPS + ('', ) # noqa

LOGGING_LEVEL = logging.DEBUG

LOGGING['loggers'][PROJECT_NAME]['level'] = LOGGING_LEVEL # noqa

TEMPLATES[0]['OPTIONS']['debug'] = True # noqa

# -----------------------------------------------------------------------------
# Django Extensions
# http://django-extensions.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

try:
    import django_extensions # noqa

    INSTALLED_APPS += ['django_extensions'] # noqa
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

try:
    import debug_toolbar # noqa

    INSTALLED_APPS += ['debug_toolbar'] # noqa
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware'] # noqa
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Local settings
# -----------------------------------------------------------------------------

try:
    from local import * # noqa
except ImportError:
    print('failed to import local settings')

    from test import * # noqa
    print('the project is running with test settings')
    print('please create a local settings file')
