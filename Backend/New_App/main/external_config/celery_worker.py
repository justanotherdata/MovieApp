from celery import Celery
#from main import app

def make_celery(app):
    #backend_url = "redis://127.0.0.1:6379/1"
    #broker_url = "redis://localhost:6379/0"
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'], broker=app.config['CELERY_BROKER_URL'])

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

#celery = make_celery(app)
#celery.conf.update({'broker_connection_retry_on_startup' : True})