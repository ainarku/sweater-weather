from django.shortcuts import render
from .models import WeatherData
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_weather_data(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            api_key = os.getenv("OPENWEATHERMAP_API_KEY")
            if not api_key:
                return render(request, 'weatherapp/error.html', {'error_message': 'API key is missing.'})


            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = json.loads(response.text)
                weather_data = WeatherData()
                weather_data.city_name = data.get('name')
                weather_data.lon = data['coord']['lon']
                weather_data.lat = data['coord']['lat']
                weather_data.temperature = data['main']['temp'] - 273.15
                weather_data.temperature_fahrenheit = (data['main']['temp'] - 273.15) * 9/5 + 32
                weather_data.feels_like = data['main']['feels_like'] - 273.15
                weather_data.weather_description = data['weather'][0]['description']
                weather_data.humidity = data['main']['humidity']
                weather_data.save()

                context = {
                    'weather_data': weather_data,
                }
                return render(request, 'weatherapp/weather_data.html', context)
            else:
                return render(request, 'weatherapp/error.html', {'error_message': 'Failed to fetch weather data.'})
        else:
            return render(request, 'weatherapp/error.html', {'error_message': 'City not provided.'})
    else:
        return render(request, 'weatherapp/location_form.html')

