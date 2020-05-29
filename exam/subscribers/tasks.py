import logging

from django.db import transaction

from exam.celery_app import celery_app
from exam.subscribers.models import Subscriber

log = logging.getLogger(__name__)


# TODO: singleton
@celery_app.task
def unhold_task():
    try:
        uuids = Subscriber.objects.filter(status=True, hold__gt=0).values_list('uuid', flat=True)
        log.info('Starting unhold task: {} subscribers to unhold'.format(len(uuids)))

        for uuid in uuids:
            try:
                with transaction.atomic():
                    subscriber = Subscriber.find(uuid=uuid, updlock=True)
                    log.info('Unholding {uuid}: holds {hold}, balance {balance}'.format(
                        uuid=subscriber.uuid, hold=subscriber.hold, balance=subscriber.balance,
                    ))
                    subscriber.unhold()
            except Exception:
                log.exception('Error in unholding {}'.format(uuid))
    except Exception:
        log.exception('Error in unhold_task')
