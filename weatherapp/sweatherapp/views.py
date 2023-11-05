from django.http import HttpResponse
from django.shortcuts import render
from .models import WeatherData
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_weather_data(request):
    city = 'Tallinn'
    if city:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return render(
                request,
                'weatherapp/error.html',
                {'error_message': 'API key is missing.'}
            )

        url = ('https://api.openweathermap.org/data'
               f'/2.5/weather?q={city}&appid={api_key}')
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            weather_data = WeatherData()
            weather_data.city_name = data.get('name')
            weather_data.temperature = data['main']['temp'] - 273.15
            weather_data.temperature_fahrenheit = (data['main']['temp'] - 273.15) * 9 / 5 + 32
            weather_data.feels_like = data['main']['feels_like'] - 273.15
            weather_data.weather_description = data.get('weather')[0].get('description')
            weather_data.humidity = data.get('main').get('humidity')
            weather_data.save()

            context = {
                'weather_data': weather_data,
            }
            return HttpResponse("Weather Data")

#   else:
#     return render(request, 'weatherapp/index.html')
