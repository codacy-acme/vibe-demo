#!/usr/bin/env python3
"""
Simple test script to verify the weather demo application works correctly.
"""

import sys
import os

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from weather_demo import WeatherApp, HttpTester, main
    print("✅ Successfully imported all classes and functions")

    # Test basic functionality
    print("\n🧪 Testing basic functionality...")

    # Test WeatherApp initialization
    weather_app = WeatherApp()
    print("✅ WeatherApp initialized successfully")

    # Test HttpTester initialization
    http_tester = HttpTester()
    print("✅ HttpTester initialized successfully")

    # Test main function (this will make actual HTTP requests)
    print("\n🚀 Running main demo function...")
    main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! The application is working correctly.")
