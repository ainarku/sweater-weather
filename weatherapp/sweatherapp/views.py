from django.shortcuts import render
from django.http import HttpResponse
from .utils import kelvin_to_celsius, kelvin_to_fahrenheit
import requests
import json
import os
from datetime import datetime
from django.utils import timezone
from dotenv import load_dotenv

load_dotenv()


def api_request(city, endpoint, temperature_unit):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return HttpResponse("OpenWeatherMap API key not found.")

    url = f'https://api.openweathermap.org/data/2.5/{endpoint}?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)

        if endpoint == "weather":
            return process_weather_data(data, temperature_unit)
        elif endpoint == "forecast":
            return process_forecast_data(data, temperature_unit)

    return None


def process_weather_data(data, temperature_unit):
    main_data = data.get('main', {})

    temperature = kelvin_to_celsius(main_data.get('temp', 0)) if temperature_unit == 'C' else kelvin_to_fahrenheit(
        main_data.get('temp', 0))
    feels_like = kelvin_to_celsius(main_data.get('feels_like', 0)) if temperature_unit == 'C' else kelvin_to_fahrenheit(
        main_data.get('feels_like', 0))

    return {
        'city_name': data.get('name'),
        'temperature': temperature,
        'feels_like': feels_like,
        'weather_description': data.get('weather', [{}])[0].get('description', 'No Description'),
        'humidity': (main_data.get('humidity', 0)),
    }


def process_forecast_data(data, temperature_unit):
    forecast_list = []

    for forecast in data.get('list', []):
        forecast_datetime = datetime.fromtimestamp(forecast.get('dt', 0))
        forecast_datetime_aware = timezone.make_aware(forecast_datetime, timezone=timezone.utc)

        main_data = forecast.get('main', {})

        if main_data:
            forecast_instance = {
                'date_time': forecast_datetime_aware,
                'temperature': kelvin_to_celsius(
                    main_data.get('temp', 0)) if temperature_unit == 'C' else kelvin_to_fahrenheit(
                    main_data.get('temp', 0)),
                'feels_like': kelvin_to_celsius(
                    main_data.get('feels_like', 0)) if temperature_unit == 'C' else kelvin_to_fahrenheit(
                    main_data.get('feels_like', 0)),
                'weather_description': forecast.get('weather', [{}])[0].get('description', 'No Description'),
                'humidity': (main_data.get('humidity', 0)),
            }
            forecast_list.append(forecast_instance)

    return forecast_list


def extract_request_data(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')
        temperature_unit = request.POST.get('temperature_unit', 'C')
        return city, temperature_unit
    return None, None


def get_weather_data(city, temperature_unit):
    current_weather = api_request(city, "weather", temperature_unit)
    forecast_data = api_request(city, "forecast", temperature_unit)

    return current_weather, forecast_data


def process_weather_view(request, template_name='weather_result.html'):
    city, temperature_unit = extract_request_data(request)

    if city and temperature_unit:
        current_weather, forecast_data = get_weather_data(city, temperature_unit)

        if current_weather and forecast_data:
            context = {
                'current_weather': current_weather,
                'forecast_data': forecast_data,
                'temperature_unit': temperature_unit,
            }

            return render(request, template_name, context)

    return HttpResponse("Method not allowed")


def fetch_weather(request):
    return process_weather_view(request, 'weather_result.html')


def search_weather(request):
    return process_weather_view(request, 'weather_result.html')


def index(request):
    return render(request, 'index.html')
