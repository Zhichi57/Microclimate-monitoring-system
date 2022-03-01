from django.contrib import admin
from django.urls import path, include
from dataDisplay.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dataDisplay.urls')),
    path('', include('dataGet.urls')),
]
