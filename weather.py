import argparse
import requests
import os

def get_city_state(zipcode):
    response = requests.get(f"http://api.zippopotam.us/us/{zipcode}")
    if response.status_code == 200:
        data = response.json()
        city = data['places'][0]['place name']
        state = data['places'][0]['state abbreviation']
        latitude = data['places'][0]['latitude']
        longitude = data['places'][0]['longitude']
        return city, state, latitude, longitude
    else:
        return None, None, None, None

def get_temperature(latitude, longitude, api_key):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&appid={api_key}")
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None

def display_zipcode(zipcode, api_key):
    city, state, latitude, longitude = get_city_state(zipcode)
    if city and state and latitude and longitude:
        temperature = get_temperature(latitude, longitude, api_key)
        if temperature is not None:
            print(f"The zipcode {zipcode} corresponds to {city}, {state}. The current temperature is {temperature}°F.")
        else:
            print(f"Could not retrieve temperature for the zipcode: {zipcode}")
    else:
        print(f"Could not find city and state for the zipcode: {zipcode}")

def main():
    parser = argparse.ArgumentParser(description="Display the city, state, and current temperature for the provided zipcode.")
    parser.add_argument("--zipcode", type=str, required=True, help="The zipcode to display")
    args = parser.parse_args()
    
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        print("Error: OPENWEATHERMAP_API_KEY environment variable not set.")
        return
    
    display_zipcode(args.zipcode, api_key)

if __name__ == "__main__":
    main()