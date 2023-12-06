# Django Weather Application

This is a weather application, built using Django, requests and OpenWeatherMap API. It allows users to access weather
information by default for the city of Tallinn or by entering a specific city name.

## Framework

The current version of the template is based on:

- Python 3.11
- Django 4.2.6

## Database

- Currently, there are applied settings for Postgres server (version 16.0) which is defined in `settings.py`. The
  developer is free to configure the settings for any database technology that business needs require.

## Git

- The template already has a `.gitignore` file, which holds all the possible folders and cache files that should not be
  pushed to the GitLab repository.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ainarku/sweater-weather.git

2. Navigate to the project directory:

   ```bash
   cd weatherapp

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

5. Set up your OpenWeatherMap API key and Database Credentials:

- Visit OpenWeatherMap (https://openweathermap.org/) to create an account.

- Obtain your API key from the dashboard.

- Specify your database user and password for the project.

- Create a file named `.env` in the project root (`sweater-weather/weatherapp`) and add the following:

   ```bash 
  # .env file
  OPENWEATHERMAP_API_KEY="your_api_key_here"
  DB_USER="your_database_user"
  DB_PASSWORD="your_database_password"

## Configuration

1. Apply migrations:
   ```bash
   python manage.py migrate

2. Start the development server:
   ```bash
   python manage.py runserver

3. Open your web browser and navigate to http://127.0.0.1:8000/ to access the app.

## Usage

- Enter the desired location in the `Enter City` search bar.
- Click the `Get Weather` button to retrieve the current weather information.
- Use the `Go back` button to start again and search for a new location.

## See the demo here:

![](/img/front_page.png "Front Page")

![](/img/result_page.png "Search Result Page")
