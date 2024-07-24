from .celery_app import celery

@celery.task
def hello_celery():
   print('HELLO')
   return 'HELLO'