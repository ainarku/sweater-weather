# Register your models here.

from django.contrib import admin
from .models import WeatherData, CustomUser

admin.site.register(WeatherData)
admin.site.register(CustomUser)