import logging

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from vkr.settings import LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


@api_view(['GET', 'POST'])
def set_sensor_info(request):
    if request.method == 'GET':
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    if request.method == 'POST':
        logger.debug(request.POST)
        if 'key' not in request.POST or 'temp' not in request.POST or 'humidity' not in request.POST:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.POST.get('temp') == 'nan' or request.POST.get('humidity') == 'nan':
            return Response(
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )

        return Response(
            data='ok',
            status=status.HTTP_202_ACCEPTED
        )
