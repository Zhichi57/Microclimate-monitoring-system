from django.urls import path, include
from dataDisplay.views import index, get_map_data, set_map_data, set_image, set_manual, add_sensor, edit_sensor, \
    delete_sensor, pdf_report, csv_report
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path(r'map_data', get_map_data, name='map_data'),
    path(r'set_map_data', set_map_data, name='set_map_data'),
    path(r'set_image', set_image, name='set_image'),
    path(r'set_manual', set_manual, name='set_manual'),
    path(r'add_sensor', add_sensor, name='add_sensor'),
    path(r'edit_sensor', edit_sensor, name='edit_sensor'),
    path(r'delete_sensor', delete_sensor, name='delete_sensor'),
    path(r'pdf_report', pdf_report, name='pdf_report'),
    path(r'csv_report', csv_report, name='csv_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
