from celery import Celery
from app.config import get_settings

settings = get_settings()

# Create Celery instance
celery_app = Celery(
    'document_processor',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=['app.tasks.document_tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,  # Results expire after 1 hour
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,  # One task at a time for heavy processing
    task_routes={
        'app.tasks.document_tasks.*': {'queue': 'documents'},
    },
)
