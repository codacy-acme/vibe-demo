#!/usr/bin/env python3
"""
Weather Information Fetcher
A demo Python application that fetches weather information from a public API
using the requests library.
"""

import json
from typing import Dict, Optional

import requests


class WeatherFetcher:
    """
    A simple weather information fetcher using OpenWeatherMap API.
    This is a demo application showcasing the use of requests library.
    """

    def __init__(self):
        # Using OpenWeatherMap's free tier (no API key required for basic city search)
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather_by_city(self, city_name: str) -> Optional[Dict]:
        """
        Fetch weather information for a given city.

        Args:
            city_name (str): Name of the city to get weather for

        Returns:
            Optional[Dict]: Weather data or None if request fails
        """
        try:
            # Note: This would normally require an API key, but we'll demonstrate
            # the structure for educational purposes
            url = f"{self.base_url}/weather"
            params = {
                'q': city_name,
                'appid': 'demo_key',  # Demo key - won't work in real requests
                'units': 'metric'
            }

            print(f"Making request to: {url}")
            print(f"Parameters: {params}")

            response = requests.get(url, params=params, timeout=10)

            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")

            if response.status_code == 200:
                return response.json()

            print(f"Error: HTTP {response.status_code}")
            print(f"Response text: {response.text}")
            return None

        except requests.exceptions.RequestException as request_error:
            print(f"Request failed: {request_error}")
            return None

    def get_public_api_demo(self) -> Optional[Dict]:
        """
        Demonstrate requests library with a public API that doesn't require authentication.
        Uses JSONPlaceholder API for demonstration.

        Returns:
            Optional[Dict]: API response data or None if request fails
        """
        try:
            url = "https://jsonplaceholder.typicode.com/posts/1"

            print(f"Making request to: {url}")

            response = requests.get(url, timeout=10)

            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")

            if response.status_code == 200:
                return response.json()

            print(f"Error: HTTP {response.status_code}")
            return None

        except requests.exceptions.RequestException as request_error:
            print(f"Request failed: {request_error}")
            return None

    def demonstrate_post_request(self) -> Optional[Dict]:
        """
        Demonstrate POST request using requests library.

        Returns:
            Optional[Dict]: API response data or None if request fails
        """
        try:
            url = "https://jsonplaceholder.typicode.com/posts"
            data = {
                'title': 'Demo Post',
                'body': 'This is a demo post created by our Python app',
                'userId': 1
            }

            print(f"Making POST request to: {url}")
            print(f"Data: {data}")

            response = requests.post(url, json=data, timeout=10)

            print(f"Response status code: {response.status_code}")

            if response.status_code == 201:  # Created
                return response.json()

            print(f"Error: HTTP {response.status_code}")
            return None

        except requests.exceptions.RequestException as request_error:
            print(f"POST request failed: {request_error}")
            return None


def main():
    """
    Main function to demonstrate the weather fetcher functionality.
    """
    print("=== Python Weather Demo Application ===")
    print(f"Using requests library version: {requests.__version__}")

    fetcher = WeatherFetcher()

    # Demonstrate GET request with public API
    print("\n1. Demonstrating GET request with JSONPlaceholder API:")
    print("-" * 50)
    result = fetcher.get_public_api_demo()
    if result:
        print("Success! Received data:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to fetch data from public API")

    # Demonstrate POST request
    print("\n2. Demonstrating POST request:")
    print("-" * 30)
    post_result = fetcher.demonstrate_post_request()
    if post_result:
        print("Success! POST response:")
        print(json.dumps(post_result, indent=2))
    else:
        print("Failed to make POST request")

    # Demonstrate weather API structure (will fail without real API key)
    print("\n3. Demonstrating weather API structure (will fail without API key):")
    print("-" * 70)
    weather_result = fetcher.get_weather_by_city("London")
    if weather_result:
        print("Weather data:")
        print(json.dumps(weather_result, indent=2))
    else:
        print("Weather API request failed (expected without valid API key)")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
