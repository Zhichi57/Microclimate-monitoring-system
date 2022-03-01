from django.urls import path, include
from dataDisplay.views import index, get_map_data, set_map_data, set_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path(r'map_data', get_map_data, name='map_data'),
    path(r'set_map_data', set_map_data, name='map_data'),
    path(r'set_image', set_image, name='map_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
