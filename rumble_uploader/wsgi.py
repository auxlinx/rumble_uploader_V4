"""
WSGI config for rumble_uploader project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rumble_uploader.settings')

# os.environ['HTTP_PROXY'] = "http://10.10.1.10:3128"
# os.environ['HTTPS_PROXY'] = "http://10.10.1.10:1080"

application = get_wsgi_application()
