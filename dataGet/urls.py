from django.urls import path, include
from .views import set_sensor_info
from django.contrib.auth import views

urlpatterns = [
    path('api/send', set_sensor_info),
]
