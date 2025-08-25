#!/usr/bin/env python3
"""
Simple CLI: look up city and state for a ZIP/postal code using api.zippopotam.us

Usage:
    python3 zip_lookup.py 90210
    python3 zip_lookup.py 90210 --country us
    python3 zip_lookup.py SW1A 1AA --country gb  # example for non-US (optional)
"""

import argparse
import json
import sys
import urllib.parse
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


API_BASE = "https://api.zippopotam.us"


def fetch_zip_data(country: str, zipcode: str, timeout: int = 10):
    country = country.lower()
    zipcode = zipcode.strip()
    url = f"{API_BASE}/{country}/{zipcode}"
    req = Request(url, headers={"User-Agent": "py-weather/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            if resp.getcode() != 200:
                return None
            payload = resp.read()
            return json.loads(payload.decode("utf-8"))
    except HTTPError as e:
        if e.code == 404:
            return None
        raise
    except URLError:
        raise


def get_current_temperature(city, state, timeout=10):
    """
    Fetch the current temperature for a city and state using wttr.in.
    Returns a string like '23°C' or '73°F', or None on failure.
    """
    # Format: City,State (spaces replaced with '+')
    location = f"{city},{state}".replace(" ", "+")
    url = f"https://wttr.in/{urllib.parse.quote(location)}?format=%t"
    try:
        with urlopen(url, timeout=timeout) as resp:
            temp = resp.read().decode("utf-8").strip()
            # wttr.in returns 'Unknown location' for bad queries
            if "Unknown location" in temp or not temp:
                return None
            # Optionally, validate temperature format (e.g., +23°C)
            if re.match(r"^[+-]?\d+°[CF]$", temp):
                return temp
            return temp  # fallback: return whatever is returned
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Get city and state for a ZIP/postal code using api.zippopotam.us"
    )
    parser.add_argument("zipcode", help="ZIP or postal code to look up")
    parser.add_argument(
        "--country",
        "-c",
        default="us",
        help="Country code (default: us). Examples: us, ca, gb, de, ...",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print all places returned (default: print first place only)",
    )
    args = parser.parse_args()

    try:
        data = fetch_zip_data(args.country, args.zipcode)
    except Exception as exc:
        print(f"Error fetching data: {exc}", file=sys.stderr)
        sys.exit(2)

    if not data:
        print(
            f"No data found for {args.zipcode} ({args.country.upper()})",
            file=sys.stderr,
        )
        sys.exit(1)

    places = data.get("places", [])
    if not places:
        print(f"No places found for {args.zipcode} in response.", file=sys.stderr)
        sys.exit(1)

    if args.all:
        for p in places:
            city = p.get("place name", "")
            state = p.get("state abbreviation", p.get("state", ""))
            print(f"{city}, {state}")
            temp = get_current_temperature(city, state)
            if temp:
                print(f"Current temperature: {temp}")
            else:
                print("Could not fetch temperature.")
    else:
        p = places[0]
        city = p.get("place name", "")
        state = p.get("state abbreviation", p.get("state", ""))
        print(f"City: {city}")
        print(f"State: {state}")
        temp = get_current_temperature(city, state)
        if temp:
            print(f"Current temperature: {temp}")
        else:
            print("Could not fetch temperature.")


if __name__ == "__main__":
    main()
