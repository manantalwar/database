"""
WSGI config for lrc_database project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lrc_database.settings")

if settings.SECRET_KEY == "":  # nosec - Bandit believes "" is a hardcoded password
    raise RuntimeError("Secret key has not been set. Refusing to launch.")

application = get_wsgi_application()
