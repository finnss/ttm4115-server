from django.contrib import admin

# Register your models here.
from .models import Sensor, Plant, User, SensorReading


class UserAdmin(admin.ModelAdmin):
     fields = ('username', 'password', 'sensor')


admin.site.register(Sensor)
admin.site.register(Plant)
admin.site.register(User)
admin.site.register(SensorReading)