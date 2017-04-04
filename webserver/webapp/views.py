from django.shortcuts import render

from django.http import HttpResponse
from .models import Sensor, User, Plant
from .forms import LoginForm


def index(request):
    """
    Planen hvis jeg får til brukere:
    current_user = ...
    sensors = Sensor.objects.get(user=current_user) #(PSEUDOKODE)
    """

    sensors = Sensor.objects.all()
    users = User.objects.all()
    plants = Plant.objects.all()
    context = {'sensors': sensors, 'users': users, 'plants': plants}
    return render(request, 'webapp/index.html', context)


def login(request):
    form = LoginForm
    context = {'form': form, 'next': '/user'}
    return render(request, 'webapp/login.html', context)