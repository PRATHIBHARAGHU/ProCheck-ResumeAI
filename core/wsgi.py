import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'runserver' command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# This is the 'application' attribute Django is looking for in the error log.
application = get_wsgi_application()