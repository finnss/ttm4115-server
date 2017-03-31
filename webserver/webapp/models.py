from __future__ import unicode_literals

from django.utils import timezone
from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=50)
    upper_moisture_bound = models.IntegerField(default=100)
    lower_moisture_bound = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    serial_number = models.CharField(max_length=50)
    monitoring_plant = models.ForeignKey(Plant, related_name='current_sensors', null=True)

    def __str__(self):
        return 'id: ' + self.serial_number


class SensorReading(models.Model):
    moisture = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    sensor = models.ForeignKey(Sensor, related_name='readings')

    def __str__(self):
        return str(self.moisture)


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    phone = models.IntegerField(blank=True, null=True)
    sensor = models.ManyToManyField(Sensor, related_name='interested_users')

    def __str__(self):
        return self.username
