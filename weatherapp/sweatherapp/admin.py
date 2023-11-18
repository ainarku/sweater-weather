from django.contrib import admin
from .models import WeatherData, WeatherNews, CustomUser, FavouriteCity, ForecastData

admin.site.register(WeatherData)
admin.site.register(CustomUser)
admin.site.register(WeatherNews)
admin.site.register(FavouriteCity)
admin.site.register(ForecastData)