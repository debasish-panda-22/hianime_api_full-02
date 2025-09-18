#!/usr/bin/env python3
"""
Simple test script to verify the HiAnime Django API is working
"""

import requests
import json
import time
import sys

def test_api():
    """Test basic API endpoints"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing HiAnime Django API...")
    print("=" * 50)
    
    # Test root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   API Name: {data.get('name', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test homepage endpoint
    print("\n2. Testing homepage endpoint...")
    try:
        response = requests.get(f"{base_url}/home/", timeout=30)
        if response.status_code == 200:
            print("✅ Homepage endpoint working")
            data = response.json()
            if data.get('success'):
                homepage_data = data.get('data', {})
                print(f"   Spotlight items: {len(homepage_data.get('spotlight', []))}")
                print(f"   Trending items: {len(homepage_data.get('trending', []))}")
                print(f"   Genres: {len(homepage_data.get('genres', []))}")
            else:
                print(f"❌ Homepage endpoint returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Homepage endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage endpoint error: {e}")
    
    # Test search endpoint
    print("\n3. Testing search endpoint...")
    try:
        response = requests.get(f"{base_url}/search/?keyword=one+piece", timeout=30)
        if response.status_code == 200:
            print("✅ Search endpoint working")
            data = response.json()
            if data.get('success'):
                search_data = data.get('data', {})
                results = search_data.get('response', [])
                print(f"   Search results: {len(results)}")
                if results:
                    print(f"   First result: {results[0].get('title', 'Unknown')}")
            else:
                print(f"❌ Search endpoint returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
    
    # Test genres endpoint
    print("\n4. Testing genres endpoint...")
    try:
        response = requests.get(f"{base_url}/genres/", timeout=10)
        if response.status_code == 200:
            print("✅ Genres endpoint working")
            data = response.json()
            if data.get('success'):
                genres = data.get('data', [])
                print(f"   Total genres: {len(genres)}")
                if genres:
                    print(f"   Sample genres: {genres[:5]}")
            else:
                print(f"❌ Genres endpoint returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Genres endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Genres endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing complete!")
    print("\n📚 API Documentation:")
    print(f"   Swagger UI: http://localhost:8000/api/v1/schema/swagger-ui/")
    print(f"   ReDoc: http://localhost:8000/api/v1/schema/redoc/")
    print(f"   Schema: http://localhost:8000/api/v1/schema/")
    
    return True

if __name__ == "__main__":
    # Wait a bit for the server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    success = test_api()
    if not success:
        sys.exit(1)