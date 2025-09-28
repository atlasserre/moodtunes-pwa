#!/usr/bin/env python3
"""
Comprehensive test cases for MoodTunes playlist search functionality
Tests both single result and multiple result scenarios
"""

import requests
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

BASE_URL = "http://127.0.0.1:5000"
SEARCH_ENDPOINT = f"{BASE_URL}/search-playlists"

def test_search(query, expected_count, expected_moods=None):
    """Test a search query and validate results"""
    print(f"\n🔍 Testing search: '{query}'")
    
    try:
        response = requests.post(SEARCH_ENDPOINT, data={"query": query})
        
        if response.status_code != 200:
            print(f"❌ HTTP Error {response.status_code}")
            return False
            
        data = response.json()
        
        if not data.get("success"):
            print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
            return False
            
        actual_count = len(data.get("moods", []))
        
        if actual_count != expected_count:
            print(f"❌ Expected {expected_count} results, got {actual_count}")
            return False
            
        print(f"✅ Found {actual_count} result(s)")
        
        # Display results
        for mood in data.get("moods", []):
            print(f"   {mood['icon']} {mood['name']} - {mood['description']}")
            
        # Validate specific moods if provided
        if expected_moods:
            actual_moods = [mood['mood_key'] for mood in data.get("moods", [])]
            for expected_mood in expected_moods:
                if expected_mood not in actual_moods:
                    print(f"❌ Expected mood '{expected_mood}' not found")
                    return False
                    
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - is the server running on {BASE_URL}?")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Run comprehensive test suite"""
    
    print(f"{Fore.CYAN}{Style.BRIGHT}🎵 MoodTunes Search Functionality Test Suite")
    print(f"{Fore.CYAN}{'='*60}")
    
    tests_passed = 0
    tests_total = 0
    
    # Test categories
    test_cases = [
        # SINGLE RESULT TESTS
        {
            "category": "Single Result Tests",
            "tests": [
                ("happy", 1, ["happy"]),
                ("sad", 1, ["sad"]),
                ("study", 1, ["focused"]),
                ("focus", 1, ["focused"]),
                ("workout", 1, ["running"]),
                ("fitness", 1, ["running"]),
                ("sleep", 1, ["sleepy"]),
                ("party", 1, ["party"]),
                ("dance", 1, ["party"]),
                ("love", 1, ["romantic"]),
                ("romance", 1, ["romantic"]),
                ("metal", 1, ["angry"]),
                ("rage", 1, ["angry"]),
                ("throwback", 1, ["nostalgic"]),
                ("2010s", 1, ["nostalgic"]),
                ("meditation", 1, ["meditative"]),
                ("zen", 1, ["meditative"]),
                ("piano", 1, ["meditative"]),
                ("melancholy", 1, ["melancholy"]),
                ("bittersweet", 1, ["melancholy"]),
                ("boost", 1, ["uplifting"]),
                ("optimistic", 1, ["uplifting"]),
                ("hustle", 1, ["motivated"]),
                ("ambition", 1, ["motivated"]),
                ("lofi", 1, ["chill"]),
                ("mellow", 1, ["chill"]),
                ("bright", 1, ["happy"]),
                ("joyful", 1, ["happy"]),
                ("cardio", 1, ["running"]),
                ("training", 1, ["running"]),
            ]
        },
        
        # MULTIPLE RESULT TESTS
        {
            "category": "Multiple Result Tests",
            "tests": [
                ("positive", 2, ["happy", "uplifting"]),
                ("calm", 2, ["chill", "meditative"]),
                ("peaceful", 2, ["chill", "meditative"]),
                ("inspiring", 2, ["motivated", "uplifting"]),
                ("energy", 2, ["energetic", "running"]),  # "energy" in energetic, "high-energy"
            ]
        },
        
        # EDGE CASES
        {
            "category": "Edge Cases",
            "tests": [
                ("xyz123", 0, []),  # No results
                ("qwerty", 0, []),  # No results
                ("", None, []),     # Empty query (should return error)
                ("a", None, []),    # Too short (should return error)
            ]
        },
        
        # PARTIAL MATCHES
        {
            "category": "Partial Match Tests",
            "tests": [
                ("relax", 1, ["chill"]),
                ("upbeat", 2, ["happy", "party"]),  # "upbeat" in happy keywords, party has "upbeat" vibes
                ("intense", 2, ["energetic", "angry"]),  # "intense" in both
                ("good", 1, ["uplifting"]),  # "good vibes"
            ]
        }
    ]
    
    # Run tests by category
    for category_data in test_cases:
        category = category_data["category"]
        tests = category_data["tests"]
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}📂 {category}")
        print(f"{Fore.GREEN}{'-' * len(category)}")
        
        for query, expected_count, expected_moods in tests:
            tests_total += 1
            
            # Handle error cases
            if expected_count is None:
                print(f"\n🔍 Testing error case: '{query}'")
                try:
                    response = requests.post(SEARCH_ENDPOINT, data={"query": query})
                    data = response.json()
                    
                    if not data.get("success"):
                        print(f"✅ Correctly returned error: {data.get('error')}")
                        tests_passed += 1
                    else:
                        print(f"❌ Should have returned error but got success")
                        
                except Exception as e:
                    print(f"❌ Unexpected error: {str(e)}")
            else:
                if test_search(query, expected_count, expected_moods):
                    tests_passed += 1
    
    # Summary
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}📊 Test Results Summary")
    print(f"{Fore.YELLOW}{'='*30}")
    print(f"Tests Passed: {Fore.GREEN}{tests_passed}")
    print(f"Tests Failed: {Fore.RED}{tests_total - tests_passed}")
    print(f"Total Tests:  {tests_total}")
    
    success_rate = (tests_passed / tests_total) * 100 if tests_total > 0 else 0
    print(f"Success Rate: {Fore.CYAN}{success_rate:.1f}%")
    
    if tests_passed == tests_total:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 All tests passed! Search functionality is working perfectly.")
        return 0
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ Some tests failed. Please check the implementation.")
        return 1

def test_server_connection():
    """Test if server is running and accessible"""
    print(f"🔗 Testing server connection to {BASE_URL}...")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print(f"   Make sure the Flask app is running with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{Style.BRIGHT}🚀 MoodTunes Search Test Suite")
    print(f"{Fore.MAGENTA}{'='*40}")
    
    # Check server connection first
    if not test_server_connection():
        sys.exit(1)
    
    # Run all tests
    exit_code = run_all_tests()
    sys.exit(exit_code)