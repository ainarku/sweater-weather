from django.contrib import admin
from .models import WeatherData, CustomUser, FavouriteCity, ForecastData

admin.site.register(WeatherData)
admin.site.register(CustomUser)
admin.site.register(FavouriteCity)
admin.site.register(ForecastData)
