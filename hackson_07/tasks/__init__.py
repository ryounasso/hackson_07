# celery_handson/celery_handson/tasks/__init__.py
from ..celery import app


@app.task()
def add_numbers(a, b):
    print('Request: {}'.format(a + b))
    return a + b
