web: gunicorn hackson_07.asgi:application --port $PORT --bind 0.0.0.0
worker: celery -A hackson_07.celery worker -l INFO -v2