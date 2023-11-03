# Create your models here.

from django.db import models

class WeatherData(models.Model):
    city_name = models.CharField(max_length=250)
    temperature_celsius = models.FloatField()
    weather_condition = models.CharField(max_length=250)
    humidity = models.FloatField()
    wind_speed = models.FloatField()


    def __str__(self):
        return self.city_name