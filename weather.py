import argparse
import requests


def get_zipcode_info(zipcode):
    api_url = f"http://api.zippopotam.us/us/{zipcode}"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description="Get information about a ZIP code.")
    parser.add_argument("zipcode", type=str, help="The ZIP code to look up.")
    args = parser.parse_args()

    zipcode_info = get_zipcode_info(args.zipcode)

    if zipcode_info:
        city = zipcode_info['places'][0]['place name']
        state = zipcode_info['places'][0]['state abbreviation']
        print(f"You are in {city}, {state}.")
    else:
        print(f"Could not retrieve information for ZIP code {args.zipcode}.")


if __name__ == "__main__":
    main()