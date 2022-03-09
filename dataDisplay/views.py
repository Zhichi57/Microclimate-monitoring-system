import csv
import datetime
import json

from fpdf import FPDF

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required

from .models import Map, Manual, UserManual, Sensor, Indications

import uuid


@login_required
def index(request):
    image = {
        'url': str(static('images/no_image.png'))[1:],
        'x': 0,
        'y': 0,
        'w': 960,
        'h': 500
    }
    floor = {
        'id': str(uuid.uuid1()),
        'name': 'Floor 1',
        'image': image,
        'zones': [],
        'sensors': []
    }
    data = {
        'floors': [floor]
    }

    obj, created = Map.objects.get_or_create(
        user_id=request.user.id,
        defaults={'map_data': json.dumps(data)},
    )

    user = User.objects.get(pk=request.user.id)
    manual = Manual.objects.all()
    sensors = Sensor.objects.filter(User=user)

    sensors_id = []
    for sensor in sensors:
        sensors_id.append(sensor.id)

    if request.GET.get('start_date') is not None:
        start_date = request.GET.get('start_date') + ' 00:00'
        end_date = request.GET.get('end_date') + ' 23:59'
        format_date = '%Y-%m-%d %H:%M'
        start_date = int(datetime.datetime.strptime(start_date, format_date).timestamp())
        end_date = int(datetime.datetime.strptime(end_date, format_date).timestamp())

        indications = Indications.objects.filter(Sensor_id__in=sensors_id, Receiving_data_time__gte=start_date,
                                                 Receiving_data_time__lte=end_date)
    else:
        indications = Indications.objects.filter(Sensor_id__in=sensors_id)

    for sensor in indications:
        date = datetime.datetime.fromtimestamp(float(sensor.Receiving_data_time))
        date = date.strftime('%H:%M:%S %d.%m.%Y')
        sensor.Receiving_data_time = date
    return render(request, 'index.html', {"manual": manual, 'sensors': sensors, 'indications': indications})


def set_image(request):
    if request.method == 'POST' and request.FILES['floor_pictures']:
        myfile = request.FILES['floor_pictures']
        fs = FileSystemStorage()
        filename = fs.save('floor_plan_' + str(request.user.id) + '.png', myfile)
        uploaded_file_url = fs.url(filename)
        user = User.objects.get(pk=request.user.id)
        set_map = Map.objects.get(user=user)
        data = json.loads(set_map.map_data)
        data['floors'][0]['image']['url'] = uploaded_file_url[1:]
        set_map.map_data = json.dumps(data)
        set_map.save()
    return redirect('/')


def get_map_data(request):
    user = User.objects.get(pk=request.user.id)
    get_map = Map.objects.get(user=user)
    data = json.loads(get_map.map_data)
    list_zones = data['floors'][0]['zones']
    # for zone in list_zones:
    #    if zone['name'] == 'test1':
    #        zone['name'] = '19.0'
    return JsonResponse(data=data)


def set_map_data(request):
    data = json.loads(request.POST.get('data', ''))
    user = User.objects.get(pk=request.user.id)
    set_map = Map.objects.get(user=user)
    set_map.map_data = json.dumps(data)
    set_map.save()
    return HttpResponse(status=200)


def set_manual(request):
    manual_id = int(request.POST.get('manual_id'))
    obj, created = UserManual.objects.update_or_create(
        user_id=request.user.id,
        defaults={'Manual_id_id': manual_id},
    )
    return HttpResponse(status=200)


def add_sensor(request):
    user = User.objects.get(pk=request.user.id)
    api_key = request.POST.get('api_key')
    sensor_name = request.POST.get('sensor_name')
    sensor_description = request.POST.get('sensor_description')
    new_sensor = Sensor(Api_key=api_key, Name=sensor_name, Description=sensor_description, User=user)
    new_sensor.save()
    return render(request, 'new_row_sensor.html', {"sensor": new_sensor})


def edit_sensor(request):
    sensor_id = request.POST.get('sensor_id')
    api_key = request.POST.get('api_key')
    sensor_name = request.POST.get('sensor_name')
    sensor_description = request.POST.get('sensor_description')
    sensor = Sensor.objects.get(id=sensor_id)
    sensor.Name = sensor_name
    sensor.Description = sensor_description
    sensor.Api_key = api_key
    sensor.save()
    return HttpResponse(status=200)


def delete_sensor(request):
    sensor_id = request.POST.get('sensor_id')
    sensor = Sensor.objects.get(id=sensor_id)
    sensor.delete()
    return HttpResponse(status=200)


def pdf_report(request):
    user = User.objects.get(pk=request.user.id)
    sensors = Sensor.objects.filter(User=user)

    sensors_id = []
    for sensor in sensors:
        sensors_id.append(sensor.id)

    if request.GET.get('start_date') is not None:
        start_date = request.GET.get('start_date') + ' 00:00'
        end_date = request.GET.get('end_date') + ' 23:59'
        format_date = '%Y-%m-%d %H:%M'
        start_date = int(datetime.datetime.strptime(start_date, format_date).timestamp())
        end_date = int(datetime.datetime.strptime(end_date, format_date).timestamp())

        indications = Indications.objects.filter(Sensor_id__in=sensors_id, Receiving_data_time__gte=start_date,
                                                 Receiving_data_time__lte=end_date)
    else:
        indications = Indications.objects.filter(Sensor_id__in=sensors_id)

    data = []
    for sensor in indications.values('Temperature', 'Humidity', 'Receiving_data_time'):
        date = datetime.datetime.fromtimestamp(float(sensor['Receiving_data_time']))
        date = date.strftime('%H:%M:%S %d.%m.%Y')
        sensor['Receiving_data_time'] = date
        data.append(list(sensor.values()))

    new_data = []
    for el in data:
        el = list(map(str, el))
        new_data.append(el)
    new_data.insert(0, ['Температура', 'Влажность', 'Дата и время'])
    spacing = 2
    pdf = FPDF()

    pdf.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.add_page()
    pdf.cell(200, 200, txt="Отчет о микроклимате", align="C", ln=1)
    if request.GET.get('start_date') is not None:
        format_date = '%Y-%m-%d'
        start_date = datetime.datetime.strptime(request.GET.get('start_date'), format_date).strftime('%d.%m.%Y')
        end_date = datetime.datetime.strptime(request.GET.get('end_date'), format_date).strftime('%d.%m.%Y')
        pdf.cell(200, -170, txt=start_date + " - " + end_date, ln=1, align="C")
    pdf.add_page()

    pdf.set_left_margin(26)

    col_width = pdf.w / 4
    row_height = pdf.font_size
    for row in new_data:
        for item in row:
            pdf.cell(col_width, row_height * spacing, txt=item, border=1)
        pdf.ln(row_height * spacing)

    pdf.output('simple_table.pdf')
    try:
        return FileResponse(open('simple_table.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def csv_report(request):
    user = User.objects.get(pk=request.user.id)
    sensors = Sensor.objects.filter(User=user)

    sensors_id = []
    for sensor in sensors:
        sensors_id.append(sensor.id)

    if request.GET.get('start_date') is not None:
        start_date = request.GET.get('start_date') + ' 00:00'
        end_date = request.GET.get('end_date') + ' 23:59'
        format_date = '%Y-%m-%d %H:%M'
        start_date = int(datetime.datetime.strptime(start_date, format_date).timestamp())
        end_date = int(datetime.datetime.strptime(end_date, format_date).timestamp())

        indications = Indications.objects.filter(Sensor_id__in=sensors_id, Receiving_data_time__gte=start_date,
                                                 Receiving_data_time__lte=end_date)
    else:
        indications = Indications.objects.filter(Sensor_id__in=sensors_id)

    data = []
    for sensor in indications.values('Temperature', 'Humidity', 'Receiving_data_time'):
        date = datetime.datetime.fromtimestamp(float(sensor['Receiving_data_time']))
        date = date.strftime('%H:%M:%S %d.%m.%Y')
        sensor['Receiving_data_time'] = date
        data.append(list(sensor.values()))

    new_data = []
    for el in data:
        el = list(map(str, el))
        new_data.append(el)

    with open('csv_report.csv', 'w', newline='', encoding='cp1251') as csv_file:
        writer = csv.writer(csv_file, dialect='excel-tab')
        writer.writerow(['Отчет о микроклимате'])
        writer.writerow([])
        if request.GET.get('start_date') is not None:
            format_date = '%Y-%m-%d'
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), format_date).strftime('%d.%m.%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), format_date).strftime('%d.%m.%Y')
            writer.writerow(['За период {} - {}'.format(start_date, end_date)])
        writer.writerow(['Температура', 'Влажность', 'Дата и время'])
        for row in new_data:
            writer.writerow(row)

    try:
        return FileResponse(open('csv_report.csv', 'rb'), content_type='text/csv')
    except FileNotFoundError:
        raise Http404()
