import argparse
import os
import requests

def get_city_state_from_zip(zipcode):
    url = f"http://api.zippopotam.us/us/{zipcode}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['places'][0]['place name']
        state = data['places'][0]['state']
        return city, state
    else:
        return "Invalid zipcode"

def get_temperature(city, state):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return "Invalid city or state"

parser = argparse.ArgumentParser(description='Get the temperature for a given zipcode')
parser.add_argument('zipcode', type=str, help='The zipcode to get the temperature for')
args = parser.parse_args()

zipcode = args.zipcode
city, state = get_city_state_from_zip(zipcode)
print(f"The city is {city} and the state is {state}")

temperature = get_temperature(city, state)
print(f"The temperature in {city}, {state} is {temperature}°F")