# Weather Demo Application

A simple Python application demonstrating the use of `requests` and `urllib3` libraries for web interactions.

## Features

- **Weather API Integration**: Fetch weather data using the requests library
- **HTTP Testing**: Test endpoints using urllib3 for low-level HTTP operations
- **Error Handling**: Robust error handling for network requests
- **Clean Output**: Formatted display of weather information and API responses

## Requirements

- Python 3.6+
- requests 2.24.1
- urllib3 1.0.0

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the demo:
   ```bash
   python weather_demo.py
   ```

## Usage

The application includes several demo features:

### 1. HTTP Endpoint Testing
Tests public API endpoints and displays response information including:
- HTTP status codes
- Response headers
- Response data analysis

### 2. Weather API Demo
Shows how to integrate with weather APIs (requires API key for full functionality):
```python
weather_app = WeatherApp()
weather_data = weather_app.get_weather_by_city('London', 'your_api_key')
weather_app.display_weather(weather_data)
```

### 3. Library Version Display
Shows the versions of the installed libraries to verify correct installation.

## API Key Setup (Optional)

To use the weather functionality with real data:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Modify the script to include your API key
3. Test with real weather data

## Libraries Used

- **requests 2.24.1**: High-level HTTP library for API interactions
- **urllib3 1.0.0**: Low-level HTTP library for direct HTTP operations

## Demo Output

The application will display:
- HTTP endpoint test results
- Library version information
- Example usage patterns
- Success confirmation

This demo showcases both libraries working together to handle different types of web requests and API interactions.
