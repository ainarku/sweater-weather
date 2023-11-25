from django.shortcuts import render
from .utils import extract_request_data, get_weather_data


def process_weather_view(request, template_name='weather_result.html'):
    city, temperature_unit = extract_request_data(request)
    context = {}

    if city and temperature_unit:
        current_weather, forecast_data = get_weather_data(
            city, temperature_unit)

        if current_weather and forecast_data:
            context = {
                'temperature': current_weather.get('temperature'),
                'current_weather': current_weather,
                'forecast_data': forecast_data,
                'temperature_unit': temperature_unit,
            }

    return render(request, template_name, context)


def fetch_weather(request):
    return process_weather_view(request, 'weather_result.html')


def search_weather(request):
    return process_weather_view(request, 'weather_result.html')


def index(request):
    default_city = 'Tallinn'
    temperature_unit = 'C'

    current_weather, forecast_data = get_weather_data(default_city,
                                                      temperature_unit)

    context = {
        'default_city': default_city,
        'weather_data': current_weather,
        'forecast': forecast_data,
        'temperature_unit': temperature_unit
    }

    return render(request, 'index.html', context)
