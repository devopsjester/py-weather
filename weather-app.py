import requests
import sys
import logging

logging.basicConfig(filename='weather-app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def get_city_state(zipcode):
    url = f"http://api.zippopotam.us/us/{zipcode}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data["places"][0]["place name"]
        state = data["places"][0]["state"]
        logging.info(f"Got city and state for zipcode {zipcode}: {city}, {state}")
        return city, state
    else:
        logging.error(f"Failed to get city and state for zipcode {zipcode}")
        return None

def get_temperature(city, state):
    api_key = "1b123c9a91468b0da3e0a39c238b2a01"  # Replace with your own API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        logging.info(f"Got temperature for {city}, {state}: {temperature}")
        return temperature
    else:
        logging.error(f"Failed to get temperature for {city}, {state}")
        return None

def get_weather(city, state):
    api_key = "1b123c9a91468b0da3e0a39c238b2a01"  # Replace with your own API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        logging.info(f"Got weather conditions for {city}, {state}: {weather}")
        return weather
    else:
        logging.error(f"Failed to get weather conditions for {city}, {state}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python weather-app.py <zipcode>")
        sys.exit(1)

    zipcode = sys.argv[1]
    city, state = get_city_state(zipcode)
    if city and state:
        temperature = get_temperature(city, state)
        weather = get_weather(city, state)
        print(f"The temperature in {city}, {state} is {temperature} degrees Fahrenheit and the weather conditions are {weather}")
    else:
        print(f"Failed to get city and state for zipcode {zipcode}")