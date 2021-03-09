web: gunicorn hackson_07.asgi:application -b 0.0.0.0:$PORT
worker: celery -A hackson_07.celery worker -l INFO -v2