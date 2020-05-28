import logging
from collections import namedtuple

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exam.api.serialization import CommonRequest, CommonResponse
from exam.model.subscriber import Subscriber, SubscriberException

log = logging.getLogger(__name__)

CommonResponseData = namedtuple(
    'CommonResponseData',
    ('result', 'status', 'description', 'addition'),
)

AdditionResponseData = namedtuple('AdditionResponseData', ('balance', 'status'))


def _create_response(response_data):
    return Response(data=CommonResponse().dump(response_data), status=response_data.status)


def _create_response_data(result=True, status=status.HTTP_200_OK, description=None, subscriber=None):
    return CommonResponseData(
        result=result, status=status, description=description,
        addition=(AdditionResponseData(balance=subscriber.balance, status=subscriber.status)
                  if subscriber else None),
    )


def subscriber_router(processor):
    def wrapper(request):
        try:
            request_data = CommonRequest().load(request.data)
            subscriber = Subscriber.find_by_uuid(request_data['addition']['uuid'])
            return processor(request_data, subscriber)
        except (ValidationError, SubscriberException) as e:
            log.exception('Bad request')
            response_data = _create_response_data(
                result=False, status=status.HTTP_400_BAD_REQUEST,
                description=repr(e),
            )
            return _create_response(response_data)
        except Exception as e:
            log.exception('Internal error')
            response_data = _create_response_data(
                result=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=repr(e),
            )
            return _create_response(response_data)
    return wrapper


@api_view(('GET',))
def ping(request):
    return Response('pong', status=status.HTTP_200_OK)


@api_view(('POST',))
@subscriber_router
def subscriber_status(request_data, subscriber):
    response_data = _create_response_data(subscriber=subscriber)
    return _create_response(response_data)


@api_view(('POST',))
@subscriber_router
def add(request_data, subscriber):
    subscriber.add(request_data['addition'].get('amount'))
    response_data = _create_response_data(subscriber=subscriber)
    return _create_response(response_data)


@api_view(('POST',))
@subscriber_router
def substract(request_data, subscriber):
    subscriber.substract(request_data['addition'].get('amount'))
    response_data = _create_response_data(subscriber=subscriber)
    return _create_response(response_data)
