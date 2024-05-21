from django.shortcuts import render
import json
import urllib.request


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        api_key = 'cc8632622c41bba41a7dd07d5d39077f'  # Replace with your Weatherstack API key

        # Construct the URL with the API key
        url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'

        try:
            # Retrieve data from the Weatherstack API
            source = urllib.request.urlopen(url).read()

            # Convert JSON data to a dictionary
            weather_data = json.loads(source)

            # Check if required keys are present in the response
            if 'error' in weather_data:
                error_message = weather_data['error']['info']
                data = {'error': error_message}
            else:
                location = weather_data.get('location', {})
                current = weather_data.get('current', {})

                # Extract relevant data from the dictionary
                data = {
                    "country_code": location.get('country', ''),
                    "coordinate": f"{location.get('longitude', '')} {location.get('latitude', '')}",
                    "temp": f"{current.get('temperature', '')}°C",
                    "pressure": current.get('pressure', ''),
                    "humidity": current.get('humidity', ''),
                }
        except urllib.error.HTTPError as e:
            # Handle HTTP errors, like 401 Unauthorized
            error_message = f"HTTP Error {e.code}: {e.reason}"
            data = {'error': error_message}
    else:
        data = {}
    return render(request, "myapp/index.html", data)

