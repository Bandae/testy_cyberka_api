"""
WSGI config for cyberka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/testy_cyberka_api/')
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberka.settings')

application = get_wsgi_application()
