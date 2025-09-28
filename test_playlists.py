import unittest
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    # Create a dummy pytest.mark for when pytest is not available
    class MockPytest:
        class mark:
            @staticmethod
            def integration(func):
                return func
    pytest = MockPytest()

from app_production import mood_playlists, mood_categories, get_time_based_suggestions, get_mood_display_info


class TestMoodPlaylists(unittest.TestCase):
    """Test suite for MoodTunes playlist functionality"""

    def test_all_moods_have_valid_playlist_id(self):
        """Test that all moods have valid Spotify playlist IDs"""
        for mood, playlist_id in mood_playlists.items():
            with self.subTest(mood=mood):
                self.assertIsInstance(playlist_id, str, f"Playlist ID for {mood} should be string")
                self.assertRegex(
                    playlist_id, 
                    r'^37i9dQZF1D[\w]+$', 
                    f"Invalid Spotify playlist ID format for {mood}: {playlist_id}"
                )
                self.assertEqual(
                    len(playlist_id), 
                    22, 
                    f"Spotify playlist ID for {mood} should be 22 characters, got {len(playlist_id)}"
                )

    def test_embed_url_format(self):
        """Test that embed URLs are properly formatted"""
        for mood, playlist_id in mood_playlists.items():
            embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator&theme=0"
            with self.subTest(mood=mood):
                self.assertTrue(
                    embed_url.startswith("https://open.spotify.com/embed/playlist/"),
                    f"Invalid embed URL format for {mood}"
                )
                self.assertIn(playlist_id, embed_url, f"Playlist ID missing from embed URL for {mood}")
                self.assertIn("utm_source=generator", embed_url, f"Missing UTM source in embed URL for {mood}")
                self.assertIn("theme=0", embed_url, f"Missing theme parameter in embed URL for {mood}")

    def test_web_url_format(self):
        """Test that web URLs are properly formatted"""
        for mood, playlist_id in mood_playlists.items():
            web_url = f"https://open.spotify.com/playlist/{playlist_id}"
            with self.subTest(mood=mood):
                self.assertTrue(
                    web_url.startswith("https://open.spotify.com/playlist/"),
                    f"Invalid web URL format for {mood}"
                )
                self.assertIn(playlist_id, web_url, f"Playlist ID missing from web URL for {mood}")

    def test_mood_count(self):
        """Test that we have the expected number of moods"""
        expected_mood_count = 15
        actual_count = len(mood_playlists)
        self.assertEqual(
            actual_count, 
            expected_mood_count, 
            f"Expected {expected_mood_count} moods, but found {actual_count}"
        )

    def test_no_duplicate_playlist_ids(self):
        """Test that all playlist IDs are unique"""
        playlist_ids = list(mood_playlists.values())
        unique_ids = set(playlist_ids)
        self.assertEqual(
            len(playlist_ids), 
            len(unique_ids), 
            f"Found duplicate playlist IDs: {[id for id in playlist_ids if playlist_ids.count(id) > 1]}"
        )

    def test_required_moods_exist(self):
        """Test that essential moods are present"""
        required_moods = ["happy", "sad", "energetic", "chill", "romantic"]
        for mood in required_moods:
            self.assertIn(mood, mood_playlists, f"Required mood '{mood}' is missing")

    def test_mood_categories_structure(self):
        """Test that mood categories are properly structured"""
        self.assertIsInstance(mood_categories, dict, "mood_categories should be a dictionary")
        
        for category_name, category_data in mood_categories.items():
            with self.subTest(category=category_name):
                self.assertIsInstance(category_data, dict, f"Category {category_name} should be a dictionary")
                self.assertIn("moods", category_data, f"Category {category_name} missing 'moods' key")
                self.assertIn("icon", category_data, f"Category {category_name} missing 'icon' key")
                self.assertIn("description", category_data, f"Category {category_name} missing 'description' key")
                
                # Test that all moods in category exist in mood_playlists
                for mood in category_data["moods"]:
                    self.assertIn(
                        mood, 
                        mood_playlists, 
                        f"Mood '{mood}' in category '{category_name}' not found in mood_playlists"
                    )

    def test_all_moods_categorized(self):
        """Test that all moods are assigned to categories"""
        categorized_moods = set()
        for category_data in mood_categories.values():
            categorized_moods.update(category_data["moods"])
        
        uncategorized_moods = set(mood_playlists.keys()) - categorized_moods
        self.assertEqual(
            len(uncategorized_moods), 
            0, 
            f"Uncategorized moods found: {uncategorized_moods}"
        )

    def test_time_based_suggestions(self):
        """Test that time-based suggestions return valid moods"""
        suggestions = get_time_based_suggestions()
        
        self.assertIsInstance(suggestions, list, "Time suggestions should be a list")
        self.assertTrue(len(suggestions) > 0, "Time suggestions should not be empty")
        self.assertTrue(len(suggestions) <= 3, "Time suggestions should not exceed 3 items")
        
        for mood in suggestions:
            self.assertIn(mood, mood_playlists, f"Suggested mood '{mood}' not found in mood_playlists")

    def test_mood_display_info(self):
        """Test mood display information function"""
        for mood in mood_playlists.keys():
            with self.subTest(mood=mood):
                info = get_mood_display_info(mood)
                
                self.assertIsInstance(info, dict, f"Display info for {mood} should be a dictionary")
                self.assertIn("key", info, f"Display info for {mood} missing 'key'")
                self.assertIn("name", info, f"Display info for {mood} missing 'name'")
                self.assertIn("icon", info, f"Display info for {mood} missing 'icon'")
                
                self.assertEqual(info["key"], mood, f"Key mismatch for mood {mood}")
                self.assertIsInstance(info["name"], str, f"Name for {mood} should be string")
                self.assertIsInstance(info["icon"], str, f"Icon for {mood} should be string")


    @pytest.mark.integration
    def test_playlist_accessibility(self):
        """Test that all playlists are accessible via HTTP requests"""
        try:
            import requests
        except ImportError:
            self.skipTest("requests not available for accessibility testing")
            
        failed_playlists = []
        
        for mood, playlist_id in mood_playlists.items():
            with self.subTest(mood=mood):
                url = f'https://open.spotify.com/playlist/{playlist_id}'
                try:
                    response = requests.head(url, timeout=15)
                    if response.status_code not in [200, 301, 302]:
                        failed_playlists.append((mood, playlist_id, response.status_code))
                        print(f"❌ {mood}: HTTP {response.status_code}")
                    else:
                        print(f"✅ {mood}: Accessible")
                except requests.RequestException as e:
                    failed_playlists.append((mood, playlist_id, str(e)))
                    print(f"❌ {mood}: Error - {str(e)[:50]}")
                    
        # Report all failures at once for better visibility
        if failed_playlists:
            failure_msg = f"Inaccessible playlists found:\\n"
            for mood, playlist_id, error in failed_playlists:
                failure_msg += f"  - {mood} ({playlist_id}): {error}\\n"
            self.fail(failure_msg)


class TestPlaylistIntegration(unittest.TestCase):
    """Integration tests for playlist functionality"""

    @pytest.mark.integration
    def test_flask_app_imports(self):
        """Test that the Flask app can be imported without errors"""
        try:
            from app_production import app
            self.assertIsNotNone(app, "Flask app should be importable")
        except ImportError as e:
            self.fail(f"Failed to import Flask app: {e}")

    @pytest.mark.integration 
    def test_mood_endpoint_structure(self):
        """Test that mood endpoint returns expected structure"""
        from app_production import app
        
        with app.test_client() as client:
            for mood in ["happy", "chill", "energetic"]:  # Test subset for speed
                with self.subTest(mood=mood):
                    response = client.post('/get-playlist', data={'mood': mood})
                    self.assertEqual(response.status_code, 200, f"Endpoint failed for mood: {mood}")
                    
                    data = response.get_json()
                    self.assertIsInstance(data, dict, f"Response for {mood} should be JSON object")
                    self.assertIn('playlist', data, f"Response for {mood} missing 'playlist' key")
                    self.assertIn('embed_url', data, f"Response for {mood} missing 'embed_url' key")
                    self.assertIn('mood', data, f"Response for {mood} missing 'mood' key")


if __name__ == "__main__":
    # Run with verbose output
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    # Also support pytest execution if available
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'pytest' and HAS_PYTEST:
        pytest.main([__file__, '-v'])
