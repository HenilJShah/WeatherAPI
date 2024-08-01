import os
from django.core.wsgi import get_wsgi_application
from mangum import Mangum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_project.settings")

application = get_wsgi_application()


def handler(event, context):
    asgi_handler = Mangum(application)
    return asgi_handler(event, context)
