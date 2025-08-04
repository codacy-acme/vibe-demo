# Python Weather Demo Application

A simple Python application that demonstrates the use of the `requests` library for making HTTP requests to various APIs.

## ⚠️ Security Warning

**IMPORTANT**: This demo application uses outdated versions of dependencies with known security vulnerabilities:

- `urllib3==1.0.0` has **1 CRITICAL** and **2 HIGH** severity CVEs
- `requests==2.24.1` has **3 MEDIUM** severity CVEs

**These versions are used for demonstration purposes only and should NOT be used in production environments.**

For production use, please update to the latest secure versions:
```
requests>=2.32.4
urllib3>=2.5.0
```

## Features

- Fetches data from public APIs using GET requests
- Demonstrates POST requests with JSON data
- Shows proper error handling for HTTP requests
- Uses specific versions of requests (2.24.1) and urllib3 (1.0.0) for demo purposes

## Requirements

- Python 3.6+
- requests==2.24.1
- urllib3==1.0.0

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python weather_app.py
```

The application will demonstrate:
1. Making GET requests to a public API (JSONPlaceholder)
2. Making POST requests with JSON data
3. Handling HTTP responses and errors
4. Displaying request/response information

## API Endpoints Used

- **JSONPlaceholder API**: A free public API for testing and prototyping
  - GET `/posts/1`: Fetches a sample post
  - POST `/posts`: Creates a new post

## Code Structure

- `WeatherFetcher` class: Main class containing API interaction methods
- `get_public_api_demo()`: Demonstrates GET requests
- `demonstrate_post_request()`: Shows POST request functionality
- `get_weather_by_city()`: Example weather API structure (requires API key)

## Notes

This is a demonstration application. The weather API functionality requires a valid API key from OpenWeatherMap to work properly.
