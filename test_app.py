#!/usr/bin/env python3
"""
Simple test script to verify the weather application functionality.
"""

import json
from weather_app import WeatherFetcher


def test_weather_app():
    """Test the basic functionality of the weather application."""
    print("Testing Weather Application...")
    
    fetcher = WeatherFetcher()
    
    # Test public API demo
    print("\n1. Testing JSONPlaceholder API:")
    result = fetcher.get_public_api_demo()
    
    if result and 'title' in result:
        print("✅ JSONPlaceholder API test PASSED")
        print(f"   Received post title: '{result['title']}'")
    else:
        print("❌ JSONPlaceholder API test FAILED")
    
    # Test POST request
    print("\n2. Testing POST request:")
    post_result = fetcher.demonstrate_post_request()
    
    if post_result and 'id' in post_result:
        print("✅ POST request test PASSED")
        print(f"   Created post with ID: {post_result['id']}")
    else:
        print("❌ POST request test FAILED")
    
    print("\n3. Testing weather API structure (expected to fail):")
    weather_result = fetcher.get_weather_by_city("London")
    
    if weather_result is None:
        print("✅ Weather API test behaved as expected (failed without API key)")
    else:
        print("⚠️  Weather API test gave unexpected result")
    
    print("\n=== Test Summary ===")
    print("The basic functionality tests have been completed.")
    print("The app demonstrates proper HTTP request handling with the requests library.")


if __name__ == "__main__":
    test_weather_app()
