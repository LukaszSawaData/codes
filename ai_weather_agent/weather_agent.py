import requests
from dotenv import load_dotenv
import os
from openai import OpenAI as genai
import openmeteo_requests
from retry_requests import retry
import pandas as pd
import requests_cache

load_dotenv()

client = genai(api_key=os.getenv("OPENAI_API_KEY"))

model = "gpt-5.2"  # Specify the newest OpenAI model

def get_weather_prompt(prompt):
    input = f"user Said: {prompt}. Your job: firstly extract the prompt. Secondly Return 'latitude, longitude' as python list with 2 String items."
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You know all cities in the world.Please return only list with longitude and latitude of the city. Do not return anything else.Does not include prompt, only list of values"},
            {"role": "user", "content": f"Extract location from: {input}"}
        ]
    )

    # Extracting the coordinates from the response
    coordinates = response.choices[0].message.content.strip()

    # Check if the response is in the expected format
    try:
        import ast  # Import ast for safe evaluation
        coordinates_list = ast.literal_eval(coordinates)  # Safely evaluate the string
        print("1:", coordinates)  # Print the evaluated list
        return [str(coord) for coord in coordinates_list]  # Ensure the coordinates are strings
    except (SyntaxError, ValueError) as e:
        print("Error parsing coordinates:", e)
        return []  # Return an empty list or handle the error as needed

def get_weather(location):
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

    # Return the weather information
    return response
# Example usage

def get_final_response(weather_info): 

    prompt = "You are expert on data structure of weather API. Needs to transform two list of temprature from API. Additionaly needs to be craeted chart with date and temprature value in lines chart" 
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. From continous data return table and charts" },
            {"role": "user", "content": f"convert data to table: {weather_info} and prepare charts"}
        ]
    )
    coordinates = response.choices[0].message.content.strip()
    print("2", coordinates) 

location = get_weather_prompt("DOes not jabe to be live data about What's the weather like in Warsaw in Poland? By weather I mean temperature, humidity and wind speed in April, 2024. If not available data, then avarage from last 5 years from your latest update.")
weather_info = get_weather(location)
get_final_response(weather_info)

