import logging
import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from vkr.settings import LOG_LEVEL
from dataDisplay.models import UserManual, Sensor, Indications, DeviationsIndications
from django.contrib.auth.models import User

from .notification import send_email

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
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.POST.get('temp') == 'nan' or request.POST.get('humidity') == 'nan':
            return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        key = request.POST.get('key')
        temp = float(request.POST.get('temp'))
        humidity = float(request.POST.get('humidity'))
        now_date = str(int(datetime.datetime.now().timestamp()))

        try:
            get_sensor = Sensor.objects.get(Api_key=key)
            user = User.objects.get(id=get_sensor.User_id)
            manual = UserManual.objects.get(user=user)
            danger_temp = False
            danger_humidity = False

            lower_humidity = float(manual.Manual_id.IndicationLimits_id.LowerHumidityLimit)
            upper_humidity = float(manual.Manual_id.IndicationLimits_id.UpperHumidityLimit)
            upper_temperature = float(manual.Manual_id.IndicationLimits_id.UpperTemperatureLimit)
            lower_temperature = float(manual.Manual_id.IndicationLimits_id.LowerTemperatureLimit)

            if humidity > upper_humidity or lower_humidity > humidity:
                danger_humidity = True

            if temp > upper_temperature or lower_temperature > temp:
                danger_temp = True

            indication = Indications(Sensor_id=get_sensor.id)
            indication.Temperature = temp
            indication.Humidity = humidity
            indication.Receiving_data_time = now_date
            indication.save()

            if danger_humidity or danger_temp:
                deviation = DeviationsIndications(Indications_id=indication)
                deviation.save()
                date = datetime.datetime.fromtimestamp(float(now_date))
                date = date.strftime('%H:%M:%S %d.%m.%Y')
                send_email(danger_temp=danger_temp, danger_humidity=danger_humidity,
                           temperature=temp, humidity=humidity, time=date, email_address=user.email)
            return Response(data='ok', status=status.HTTP_202_ACCEPTED)
        except Sensor.DoesNotExist:
            return Response(data='no sensor', status=status.HTTP_202_ACCEPTED)

