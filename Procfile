web: daphne hackson_07.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery --app hackson_07.celery worker -l INFO