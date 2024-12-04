import os
import requests
import sys


# Function to get latitude and longitude based on a ZIP code
def get_lat_long(zip_code):
    # API endpoint for getting geolocation data
    url = f"http://api.zippopotam.us/us/{zip_code}"
    # Send a GET request to the API
    response = requests.get(url)
    # If the request is successful
    if response.status_code == 200:
        data = response.json()
        # Extract latitude and longitude from the response
        latitude = data["places"][0]["latitude"]
        longitude = data["places"][0]["longitude"]
        return latitude, longitude
    else:
        # Return None if the request fails
        return None, None


# Function to get weather conditions and temperature based on latitude and longitude
def get_weather_conditions(latitude, longitude):
    # API endpoint for getting weather data from wttr.in
    url = f"http://wttr.in/{latitude},{longitude}?format=%C+%t"
    # Send a GET request to the API
    response = requests.get(url)
    # If the request is successful
    if response.status_code == 200:
        # Return weather conditions and temperature
        return response.text.strip()
    else:
        # Return error message if the request fails
        return "Weather conditions could not be retrieved."


# Main execution block
if __name__ == "__main__":
    # Check if ZIP code is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <ZIP-code>")
    else:
        # Placeholder for the rest of the script logic
        zip_code = sys.argv[1]
        latitude, longitude = get_lat_long(zip_code)
        if latitude and longitude:
            weather_conditions = get_weather_conditions(latitude, longitude)
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print(f"Weather Conditions: {weather_conditions}")
        else:
            print("Error: ZIP code not found or API request failed.")
