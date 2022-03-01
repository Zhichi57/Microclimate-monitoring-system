import json

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from .models import Map

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
    return render(request, 'index.html', {"foo": "bar"})


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
    for zone in list_zones:
        if zone['name'] == 'test1':
            zone['name'] = '19.0'
    return JsonResponse(data=data)


def set_map_data(request):
    data = json.loads(request.POST.get('data', ''))
    user = User.objects.get(pk=request.user.id)
    set_map = Map.objects.get(user=user)
    set_map.map_data = json.dumps(data)
    set_map.save()
    return HttpResponse(status=200)
