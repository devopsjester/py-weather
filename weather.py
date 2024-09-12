"""
Weather CLI Script

This script provides a command-line interface (CLI) to display the city, state,
latitude, longitude, and current temperature for a given zipcode. It uses the Zippopotam.us API to fetch
location information based on the provided zipcode and a weather API to fetch the current temperature.

Usage:
    python weather.py --zipcode <zipcode> --unit <unit>

Example:
    python weather.py --zipcode 90210 --unit celsius

Dependencies:
    - argparse: For parsing command-line arguments.
    - requests: For making HTTP requests to the Zippopotam.us API and the weather API.
    - os: For accessing environment variables.

Functions:
    - get_location_info(zipcode): Fetches city, state, latitude, and longitude information for the given zipcode.
    - get_current_temperature(latitude, longitude, unit): Fetches the current temperature for the given coordinates.
    - main(): Parses command-line arguments and displays the location information and current temperature.

Author:
    Your Name
"""

import argparse
import requests
import os

def get_location_info(zipcode):
    """
    Fetches city, state, latitude, and longitude information for the given zipcode using the Zippopotam.us API.

    Args:
        zipcode (str): The zipcode for which to fetch the location information.

    Returns:
        tuple: A tuple containing the city, state, latitude, and longitude corresponding to the provided zipcode.
               Returns (None, None, None, None) if the zipcode is invalid or the API request fails.
    """
    api_url = f"http://api.zippopotam.us/us/{zipcode}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        city = data['places'][0]['place name']
        state = data['places'][0]['state']
        latitude = data['places'][0]['latitude']
        longitude = data['places'][0]['longitude']
        return city, state, latitude, longitude
    else:
        return None, None, None, None

def get_current_temperature(latitude, longitude, unit):
    """
    Fetches the current temperature for the given coordinates using a weather API.

    Args:
        latitude (str): The latitude of the location.
        longitude (str): The longitude of the location.
        unit (str): The unit for temperature ('celsius' or 'fahrenheit').

    Returns:
        float: The current temperature in the specified unit.
               Returns None if the API request fails.
    """
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the OPENWEATHERMAP_API_KEY environment variable.")
    
    units = 'metric' if unit == 'celsius' else 'imperial'
    api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units={units}&appid={api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None

def main():
    """
    Parses command-line arguments and displays the city, state, latitude, longitude, and current temperature for the provided zipcode.

    This function sets up the argument parser, retrieves the zipcode and unit from the command-line
    arguments, fetches the location information using the get_location_info function, fetches
    the current temperature using the get_current_temperature function, and prints the information
    to the console.
    """
    parser = argparse.ArgumentParser(
        description="CLI app to display the city, state, latitude, longitude, and current temperature for the provided zipcode"
    )
    parser.add_argument("--zipcode", type=str, required=True, help="Zipcode to display")
    parser.add_argument("--unit", type=str, choices=['celsius', 'fahrenheit'], default='celsius', help="Unit for temperature (celsius or fahrenheit)")
    args = parser.parse_args()

    city, state, latitude, longitude = get_location_info(args.zipcode)
    if city and state and latitude and longitude:
        print(f"The provided zipcode {args.zipcode} corresponds to {city}, {state}.")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        
        temperature = get_current_temperature(latitude, longitude, args.unit)
        if temperature is not None:
            unit_symbol = '°C' if args.unit == 'celsius' else '°F'
            print(f"Current Temperature: {temperature}{unit_symbol}")
        else:
            print("Could not fetch the current temperature.")
    else:
        print(f"Invalid zipcode: {args.zipcode}")

if __name__ == "__main__":
    main()