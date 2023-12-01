import os
import requests
import json
from datetime import datetime
from django.http import HttpResponse
from django.utils import timezone
from dotenv import load_dotenv

load_dotenv()


def api_request(city, endpoint, temperature_unit):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    if not api_key:
        return HttpResponse("Weather data is currently unavailable. Please try again later.")

    url = f'https://api.openweathermap.org/data/2.5/{endpoint}?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)

        if endpoint == "weather":
            return process_weather_data(data, temperature_unit)
        elif endpoint == "forecast":
            return process_forecast_data(data, temperature_unit)

    return HttpResponse(f"Error: Unable to fetch {endpoint} data for {city}. Please try again later.")


def process_weather_data(data, temperature_unit):
    main_data = data.get('main', {})
    weather_info = data.get('weather', [{}])[0]

    temperature = convert_temperature(main_data.get('temp', 0), temperature_unit)
    feels_like = convert_temperature(main_data.get('feels_like', 0), temperature_unit)

    return {
        'city_name': data.get('name'),
        'temperature': temperature,
        'feels_like': feels_like,
        'weather_description': data.get('weather', [{}])[0].get(
            'description', 'No Description'),
        'weather_icon': weather_info.get('icon', ''),
        'humidity': (main_data.get('humidity', 0)),
    }


def process_forecast_data(data, temperature_unit):
    forecast_list = []

    dates_set = set()

    for forecast in data.get('list', []):
        forecast_datetime = datetime.fromtimestamp(forecast.get('dt', 0))
        forecast_datetime_aware = timezone.make_aware(
            forecast_datetime, timezone=timezone.utc)

        date_str = forecast_datetime_aware.strftime('%Y-%m-%d')

        if date_str in dates_set:
            continue

        dates_set.add(date_str)

        if forecast_datetime.date() == datetime.now().date():
            continue

        main_data = forecast.get('main', {})
        weather_data = forecast.get('weather', [{}])[0]

        if main_data and weather_data:
            forecast_instance = {
                'date_time': forecast_datetime_aware,
                'temperature': convert_temperature(main_data.get('temp', 0), temperature_unit),
                'feels_like': convert_temperature(main_data.get('feels_like', 0), temperature_unit),
                'weather_description': weather_data.get('description', 'No Description'),
                'weather_icon': weather_data.get('icon', '01d'),  # Assuming '01d' as a default icon code
                'humidity': main_data.get('humidity', 0),
            }
            forecast_list.append(forecast_instance)

    return forecast_list


def convert_temperature(kelvin, target_unit):
    celsius = kelvin_to_celsius(kelvin)
    if target_unit == 'C':
        return celsius
    else:
        return kelvin_to_fahrenheit(kelvin)


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


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32
