import logging

from exam.celery_app import celery_app
from exam.model.subscriber import Subscriber

log = logging.getLogger(__name__)


# TODO: singleton
@celery_app.task
def unhold_task():
    queryset = Subscriber.objects.filter(status=True, hold__gt=0)
    log.info("Starting unhold task: {} subscribers to unhold".format(queryset.count()))

    for subscriber in queryset:
        try:
            log.info('Unholding {uuid}: holds {hold}, balance {balance}'.format(
                uuid=subscriber.uuid, hold=subscriber.hold, balance=subscriber.balance,
            ))
            subscriber.unhold()
        except Exception:
            log.exception('Error in unholding {}'.format(subscriber.uuid))
