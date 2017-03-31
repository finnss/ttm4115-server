from django.shortcuts import render

from django.http import HttpResponse
from .models import Sensor


def index(request):
    sensors = Sensor.objects.all()
    context = {'sensors': sensors}
    return render(request, 'webapp/index.html', context)