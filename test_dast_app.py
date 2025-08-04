#!/usr/bin/env python3
"""
Test script for the DAST Demo Application
"""
import requests
import time
import sys


def test_application(base_url="http://localhost:3008"):
    """Test all endpoints of the application."""
    endpoints = [
        "/",
        "/about",
        "/contact",
        "/api/health",
        "/robots.txt",
        "/sitemap.xml"
    ]
    
    print(f"Testing application at {base_url}")
    print("-" * 50)
    
    all_passed = True
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            status = "✓ PASS" if response.status_code == 200 else f"✗ FAIL ({response.status_code})"
            print(f"{endpoint:<15} - {status}")
            
            if response.status_code != 200:
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"{endpoint:<15} - ✗ FAIL (Connection Error: {e})")
            all_passed = False
    
    # Test POST endpoint
    try:
        response = requests.post(
            f"{base_url}/contact",
            data={"name": "Test User", "email": "test@example.com", "message": "Test message"},
            timeout=10
        )
        status = "✓ PASS" if response.status_code == 200 else f"✗ FAIL ({response.status_code})"
        print(f"{'POST /contact':<15} - {status}")
        
        if response.status_code != 200:
            all_passed = False
            
    except requests.exceptions.RequestException as e:
        print(f"{'POST /contact':<15} - ✗ FAIL (Connection Error: {e})")
        all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1


def wait_for_app(base_url="http://localhost:3008", max_attempts=30):
    """Wait for the application to be ready."""
    print(f"Waiting for application at {base_url} to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print(f"✓ Application is ready after {attempt + 1} attempts")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
    
    print(f"✗ Application failed to start after {max_attempts} attempts")
    return False


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
    
    # Wait for app to be ready
    if not wait_for_app(base_url):
        sys.exit(1)
    
    # Run tests
    sys.exit(test_application(base_url))
