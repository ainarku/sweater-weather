from django.contrib import admin
from .models import WeatherData, News, CustomUser

admin.site.register(WeatherData)
admin.site.register(CustomUser)
admin.site.register(News)
