from django.contrib import admin
from .models import WeatherData, News, CustomUser, UserPreference, FavouriteCity, ForecastData

admin.site.register(WeatherData)
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(UserPreference)
admin.site.register(FavouriteCity)
admin.site.register(ForecastData)