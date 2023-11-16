from django.http import HttpResponse
from django.shortcuts import render
from .models import WeatherData, UserPreference
from .utils import kelvin_to_celsius, kelvin_to_fahrenheit, humidity_to_percentage
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_weather_data(request):
    user_city = 'Tallinn'

    if user_city:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return render(
                request,
                'weatherapp/error.html',
                {'error_message': 'API key is missing.'}
            )

        url = f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)

            if request.user is not None and request.user.is_authenticated:
                user_preference, created = UserPreference.objects.get_or_create(
                    user=request.user, defaults={'temperature_unit': 'C'}
                )
                weather_data = WeatherData(user_preference=user_preference)
            else:
                return HttpResponse("User not authenticated")

            weather_data.city_name = data.get('name')

            if user_preference.temperature_unit == 'C':
                weather_data.temperature = kelvin_to_celsius(data.get('main', {}).get('temp', 0))
                weather_data.feels_like = kelvin_to_celsius(data.get('main', {}).get('feels_like', 0))
                weather_data.temperature_fahrenheit = kelvin_to_fahrenheit(data.get('main', {}).get('temp', 0))
            else:
                weather_data.temperature = kelvin_to_fahrenheit(data.get('main', {}).get('temp', 0))
                weather_data.feels_like = kelvin_to_fahrenheit(data.get('main', {}).get('feels_like', 0))
                weather_data.temperature_fahrenheit = data.get('main', {}).get('temp', 0)

            weather_data.weather_description = data.get('weather', [{}])[0].get('description', 'No Description')

            humidity_percentage = humidity_to_percentage(data.get('main', {}).get('humidity', 0))
            weather_data.humidity = humidity_percentage

            weather_data.save()

            context = {
                'weather_data': weather_data,
                'user_preference': user_preference,
            }

            return HttpResponse("Weather Data")

    return HttpResponse("User's city not provided")


#   else:
#     return render(request, 'weatherapp/index.html')

def home(request):
    return render(request, 'home.html')


def search_weather(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        # Perform the weather search or any other processing here
        # You can use the 'city' variable to get the user input

        # For demonstration purposes, let's pass the city to the template
        return render(request, 'weather_result.html', {'city': city})
