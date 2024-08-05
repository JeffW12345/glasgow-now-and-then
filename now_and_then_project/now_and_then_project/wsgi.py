"""
WSGI config for now_and_then_project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to the sys.path
path = '/home/nowandthen/glasgow-now-and-then/now_and_then_project'
if path not in sys.path:
    sys.path.append(path)

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'now_and_then_project.settings')

from django.core.wsgi import get_wsgi_application

# Create the WSGI application object
application = get_wsgi_application()