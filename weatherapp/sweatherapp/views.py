from django.http import HttpResponse
from django.shortcuts import render
from .models import WeatherData, UserPreference, ForecastData
from .utils import kelvin_to_celsius, kelvin_to_fahrenheit, humidity_to_percentage
import requests
import json
import os
from datetime import datetime
from django.utils import timezone
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

        # Fetch current weather data
        current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        current_response = requests.get(current_url)

        if current_response.status_code == 200:
            current_data = json.loads(current_response.text)

            # Fetch forecast data
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
            forecast_response = requests.get(forecast_url)

            if forecast_response.status_code == 200:
                forecast_data = json.loads(forecast_response.text)

                # Save current weather data
                user_preference, created = UserPreference.objects.get_or_create(
                    user=request.user, defaults={'temperature_unit': 'C'}
                )
                weather_data = WeatherData(user_preference=user_preference)
                weather_data.city_name = current_data.get('name')

                if user_preference.temperature_unit == 'C':
                    weather_data.temperature = kelvin_to_celsius(current_data.get('main', {}).get('temp', 0))
                    weather_data.feels_like = kelvin_to_celsius(current_data.get('main', {}).get('feels_like', 0))
                    weather_data.temperature_fahrenheit = kelvin_to_fahrenheit(
                        current_data.get('main', {}).get('temp', 0))
                else:
                    weather_data.temperature = kelvin_to_fahrenheit(current_data.get('main', {}).get('temp', 0))
                    weather_data.feels_like = kelvin_to_fahrenheit(current_data.get('main', {}).get('feels_like', 0))
                    weather_data.temperature_fahrenheit = current_data.get('main', {}).get('temp', 0)

                weather_data.weather_description = current_data.get('weather', [{}])[0].get('description',
                                                                                            'No Description')
                humidity_percentage = humidity_to_percentage(current_data.get('main', {}).get('humidity', 0))
                weather_data.humidity = humidity_percentage
                weather_data.save()

                # Save forecast data
                for forecast in forecast_data.get('list', []):
                    forecast_datetime = datetime.fromtimestamp(forecast.get('dt', 0))
                    forecast_datetime_aware = timezone.make_aware(forecast_datetime, timezone=timezone.utc)

                    main_data = forecast.get('main', {})

                    if main_data:
                        forecast_instance = ForecastData(
                            city_name=forecast_data.get('city', {}).get('name'),
                            date_time=forecast_datetime_aware,
                            temperature=kelvin_to_celsius(main_data.get('temp', 0)),
                            temperature_fahrenheit=kelvin_to_fahrenheit(main_data.get('temp', 0)),
                            feels_like=kelvin_to_celsius(main_data.get('feels_like', 0)),
                            weather_description=forecast.get('weather', [{}])[0].get('description', 'No Description'),
                            humidity=humidity_to_percentage(main_data.get('humidity', 0)),
                            user_preference=user_preference,
                        )
                        forecast_instance.save()
                context = {
                    'weather_data': weather_data,
                    'user_preference': user_preference,
                }

                return HttpResponse("Weather Data and Forecast Data saved successfully")

    return HttpResponse("User's city not provided")


def home(request):
    return render(request, 'home.html')


def search_weather(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        # Perform the weather search or any other processing here
        # You can use the 'city' variable to get the user input

        # For demonstration purposes, let's pass the city to the template
        return render(request, 'weather_result.html', {'city': city})
