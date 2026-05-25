import requests

def get_weather_forecast(location):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location[0],
        "longitude": location[1],
        "hourly": "temperature_2m",
    }

    # Making the API call
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}

# Example usage
location = ["52.2297", "21.0122"]
weather_data = get_weather_forecast(location)
print(weather_data)