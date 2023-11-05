from django.db import models


class WeatherData(models.Model):
    city_name = models.CharField(max_length=255, blank=False, null=False)
    temperature = models.FloatField(blank=False, null=False)
    temperature_fahrenheit = models.FloatField(blank=False, null=False)
    feels_like = models.FloatField(blank=False, null=True)
    weather_description = models.CharField(max_length=255, blank=False, null=False)
    humidity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return (f"Weather in {self.city_name}: {self.temperature}°C - "
                f"{self.temperature_fahrenheit}°F - {self.weather_description}")


class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
