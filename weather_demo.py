#!/usr/bin/env python3
"""
Weather Info Demo Application

A simple Python application that demonstrates the use of requests and urllib3 libraries
to fetch weather information and perform web requests.

Features:
- Fetch current weather data from a public API
- Parse and display weather information
- Handle HTTP requests with custom headers
- Error handling for network requests
"""

import json
from typing import Dict, Optional

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for demo purposes
urllib3.disable_warnings(InsecureRequestWarning)


class WeatherApp:
    """A simple weather application using requests library."""

    def __init__(self):
        """Initialize the weather app."""
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WeatherDemo/1.0'
        })

    def get_weather_by_city(self, city: str, api_key: str) -> Optional[Dict]:
        """
        Fetch weather data for a specific city.

        Args:
            city: The name of the city
            api_key: OpenWeatherMap API key

        Returns:
            Weather data dictionary or None if request fails
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def display_weather(self, weather_data: Dict) -> None:
        """
        Display weather information in a formatted way.

        Args:
            weather_data: Weather data dictionary
        """
        if not weather_data:
            print("No weather data to display")
            return

        city = weather_data.get('name', 'Unknown')
        country = weather_data.get('sys', {}).get('country', 'Unknown')
        temp = weather_data.get('main', {}).get('temp', 'N/A')
        description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
        humidity = weather_data.get('main', {}).get('humidity', 'N/A')

        print(f"\n🌤️  Weather in {city}, {country}")
        print(f"Temperature: {temp}°C")
        print(f"Description: {description.title()}")
        print(f"Humidity: {humidity}%")


class HttpTester:
    """A simple HTTP testing utility using urllib3."""

    def __init__(self):
        """Initialize the HTTP tester."""
        self.http = urllib3.PoolManager()

    def test_endpoint(self, url: str) -> None:
        """
        Test an HTTP endpoint and display response information.

        Args:
            url: The URL to test
        """
        try:
            print(f"\n🔍 Testing endpoint: {url}")

            response = self.http.request('GET', url)

            print(f"Status: {response.status}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response length: {len(response.data)} bytes")

            # Try to parse as JSON if possible
            try:
                data = json.loads(response.data.decode('utf-8'))
                print("Response type: JSON")
                if isinstance(data, dict) and len(data) <= 5:
                    print(f"Sample data: {data}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("Response type: Non-JSON")

        except urllib3.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Data parsing error: {e}")


def main():
    """Main application entry point."""
    print("🐍 Python Weather Demo Application")
    print("Using requests 2.24.1 and urllib3 1.0.0")
    print("=" * 50)

    # Initialize HTTP tester
    http_tester = HttpTester()

    # Demo 1: Test a public API endpoint
    print("\n📡 Demo 1: Testing public API endpoints")
    test_urls = [
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1"
    ]

    for url in test_urls:
        http_tester.test_endpoint(url)

    # Demo 2: Weather API (would need API key for real use)
    print("\n🌦️  Demo 2: Weather API Demo")
    print("Note: To use weather functionality, you need an OpenWeatherMap API key")
    print("Example usage:")
    print("  weather_app = WeatherApp()")
    print("  weather_data = weather_app.get_weather_by_city('London', 'your_api_key')")
    print("  weather_app.display_weather(weather_data)")

    # Demo 3: Show library versions
    print("\n📚 Library versions:")
    print("  requests: " + requests.__version__)
    print("  urllib3: " + urllib3.__version__)

    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
