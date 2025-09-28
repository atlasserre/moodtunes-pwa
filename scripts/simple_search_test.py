#!/usr/bin/env python3
"""
Simple test cases for MoodTunes search functionality
Tests key scenarios to verify the search is working correctly
"""

import subprocess
import json
import sys


def execute_curl_request(query):
    """Execute curl request to search endpoint.

    Args:
        query: Search query string

    Returns:
        tuple: (success, data) where success is bool and data is parsed JSON
    """
    cmd = f'curl -s -X POST -d "query={query}" http://127.0.0.1:5000/search-playlists'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Curl failed with exit code {result.returncode}")
        return False, None

    if not result.stdout.strip():
        print(f"❌ No response from server")
        return False, None

    try:
        data = json.loads(result.stdout)
        return True, data
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON response: {result.stdout[:100]}...")
        return False, None


def validate_search_response(data, expected_count):
    """Validate search response data and count.

    Args:
        data: Parsed JSON response data
        expected_count: Expected number of results

    Returns:
        bool: True if validation passes
    """
    if not data.get("success"):
        if expected_count == 0:
            print(f"✅ Correctly returned error: {data.get('error', 'Unknown error')}")
            return True
        else:
            print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
            return False

    actual_count = len(data.get("moods", []))

    if actual_count != expected_count:
        print(f"❌ Expected {expected_count} results, got {actual_count}")
        if actual_count > 0:
            print("   Found:")
            for mood in data.get("moods", []):
                print(f"   - {mood.get('name', 'Unknown')}")
        return False

    return True


def display_results(data):
    """Display search results in formatted output.

    Args:
        data: Parsed JSON response containing mood results
    """
    actual_count = len(data.get("moods", []))
    print(f"✅ Found {actual_count} result(s)")

    for mood in data.get("moods", []):
        print(f"   - {mood.get('name', 'Unknown')}: {mood.get('description', 'No description')}")


def run_curl_test(query, expected_count):
    """Test search using curl command with comprehensive validation.

    Executes a curl-based search request and validates the response
    structure, success status, and result count.

    Args:
        query (str): Search query to test
        expected_count (int): Expected number of results

    Returns:
        bool: True if test passes, False otherwise
    """
    print(f"\n🔍 Testing: '{query}'")

    try:
        # Execute curl request
        success, data = execute_curl_request(query)
        if not success:
            return False

        # Validate response
        if not validate_search_response(data, expected_count):
            return False

        # Display results if successful
        if data.get("success"):
            display_results(data)

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run key test cases"""

    print("🎵 MoodTunes Search Functionality Tests")
    print("=" * 45)

    # Test cases: (query, expected_count)
    test_cases = [
        # Single result tests
        ("happy", 1),
        ("study", 1),  # Should find "focused"
        ("workout", 1),  # Should find "running"
        ("meditation", 1),  # Should find "meditative"
        # Multiple result tests
        ("positive", 2),  # Should find "happy" and "uplifting"
        ("calm", 2),  # Should find "chill" and "meditative"
        ("peaceful", 2),  # Should find "chill" and "meditative"
        ("inspiring", 2),  # Should find "motivated" and "uplifting"
        # No results
        ("xyz123", 0),
        # Error cases will need manual testing
    ]

    passed = 0
    total = len(test_cases)

    for query, expected_count in test_cases:
        if run_curl_test(query, expected_count):
            passed += 1

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
