import argparse
import os
import requests

def get_zipcode_info(zipcode):
    api_url = f"http://api.zippopotam.us/us/{zipcode}"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_info(lat, lon, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="Get information about a ZIP code.")
    parser.add_argument("zipcode", type=str, help="The ZIP code to look up.")
    args = parser.parse_args()

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        print("Error: OPENWEATHERMAP_API_KEY environment variable not set.")
        return

    zipcode_info = get_zipcode_info(args.zipcode)

    if zipcode_info:
        city = zipcode_info["places"][0]["place name"]
        state = zipcode_info["places"][0]["state abbreviation"]
        lat = zipcode_info["places"][0]["latitude"]
        lon = zipcode_info["places"][0]["longitude"]

        weather_info = get_weather_info(lat, lon, api_key)

        if weather_info:
            temperature = weather_info["main"]["temp"]
            print(f"You are in {city}, {state}. The temperature is {temperature}°F.")
        else:
            print(f"Could not retrieve weather information for {city}, {state}.")
    else:
        print(f"Could not retrieve information for ZIP code {args.zipcode}.")

if __name__ == "__main__":
    main()