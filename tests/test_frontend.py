"""
Frontend Integration Tests for MoodTunes
Tests the actual HTML/CSS/JS integration to catch UI regressions
"""
import unittest
from app import app
from bs4 import BeautifulSoup


class TestFrontendIntegration(unittest.TestCase):
    """Test frontend UI elements and integration"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        
    def test_search_input_element_exists(self):
        """Test that search input field exists with correct attributes"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for search input element
        search_input = soup.find('input', {'id': 'search-input'})
        self.assertIsNotNone(search_input, "Search input field with id='search-input' not found")
        
        # Verify input attributes
        self.assertEqual(search_input.get('type'), 'text', "Search input should be type='text'")
        self.assertEqual(search_input.get('class'), ['search-input'], "Search input should have class='search-input'")
        self.assertIsNotNone(search_input.get('placeholder'), "Search input should have placeholder text")
        self.assertEqual(search_input.get('autocomplete'), 'off', "Search input should have autocomplete='off'")
        
    def test_search_button_element_exists(self):
        """Test that search button exists with correct attributes"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for search button
        search_button = soup.find('button', {'id': 'search-btn'})
        self.assertIsNotNone(search_button, "Search button with id='search-btn' not found")
        
        # Verify button attributes
        self.assertEqual(search_button.get('type'), 'button', "Search button should be type='button'")
        self.assertEqual(search_button.get('class'), ['search-button'], "Search button should have class='search-button'")
        
    def test_search_results_container_exists(self):
        """Test that search results container exists"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for search results container
        search_results = soup.find('div', {'id': 'search-results'})
        self.assertIsNotNone(search_results, "Search results container with id='search-results' not found")
        
        # Check for search results list
        search_results_list = soup.find('div', {'id': 'search-results-list'})
        self.assertIsNotNone(search_results_list, "Search results list with id='search-results-list' not found")
        
        # Check for loading indicator
        search_loading = soup.find('div', {'id': 'search-loading'})
        self.assertIsNotNone(search_loading, "Search loading indicator with id='search-loading' not found")
        
    def test_version_badge_exists(self):
        """Test that version badge is present and properly formatted"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for version badge
        version_badge = soup.find('div', {'class': 'version-badge'})
        self.assertIsNotNone(version_badge, "Version badge with class='version-badge' not found")
        
        # Verify version content
        version_text = version_badge.get_text().strip()
        self.assertTrue(version_text.startswith('v'), f"Version badge should start with 'v', got: {version_text}")
        self.assertRegex(version_text, r'v\d+\.\d+\.\d+', f"Version should match pattern vX.Y.Z, got: {version_text}")
        
        # Verify tooltip
        title = version_badge.get('title')
        self.assertIsNotNone(title, "Version badge should have title attribute")
        self.assertIn('App Version:', title, "Title should contain 'App Version:'")
        self.assertIn('Build:', title, "Title should contain 'Build:'")
        
    def test_search_form_structure(self):
        """Test that search form has proper structure"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find search container
        search_container = soup.find('div', {'class': 'search-container'})
        self.assertIsNotNone(search_container, "Search container not found")
        
        # Verify it contains both input and button
        input_in_container = search_container.find('input', {'id': 'search-input'})
        button_in_container = search_container.find('button', {'id': 'search-btn'})
        
        self.assertIsNotNone(input_in_container, "Search input should be inside search container")
        self.assertIsNotNone(button_in_container, "Search button should be inside search container")
        
    def test_javascript_files_included(self):
        """Test that required JavaScript files are included"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for script includes
        script_tags = soup.find_all('script', src=True)
        script_sources = [script.get('src') for script in script_tags]
        
        required_scripts = ['/static/script.js', '/static/pwa.js']
        for required_script in required_scripts:
            self.assertIn(required_script, script_sources, 
                         f"Required script {required_script} not found in page")
            
    def test_css_files_included(self):
        """Test that required CSS files are included"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for CSS links
        link_tags = soup.find_all('link', rel='stylesheet')
        css_sources = [link.get('href') for link in link_tags]
        
        self.assertIn('/static/style.css', css_sources, "Required CSS file not found")
        
    def test_no_malformed_html_attributes(self):
        """Test that there are no malformed HTML attributes like orphaned placeholder text"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        
        # Check for common malformation patterns that caused the original bug
        malformed_patterns = [
            # These patterns should not appear as standalone text
            'placeholder="Try \'workout\', \'chill\', \'study\', or \'jazz\'..."\n           aria-label=',
            'aria-label="Search playlists"\n           autocomplete=',
            'autocomplete="off">\n    <button'
        ]
        
        # These patterns should not appear as standalone text (would indicate malformed HTML)
        for pattern in malformed_patterns:
            self.assertNotIn(pattern, html, f"Found malformed HTML pattern: {pattern[:50]}...")
        
    def test_search_section_completeness(self):
        """Test that the search section is complete with all expected elements"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find search section
        search_section = soup.find('div', {'class': 'search-section'})
        self.assertIsNotNone(search_section, "Search section not found")
        
        # Check for all expected child elements
        search_title = search_section.find('h2', {'class': 'search-title'})
        self.assertIsNotNone(search_title, "Search title not found")
        
        search_container = search_section.find('div', {'class': 'search-container'})
        self.assertIsNotNone(search_container, "Search container not found")
        
        search_results = search_section.find('div', {'id': 'search-results'})
        self.assertIsNotNone(search_results, "Search results container not found")
        
    def test_mood_selection_form_exists(self):
        """Test that the mood selection form exists and is properly structured"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for mood form
        mood_form = soup.find('form', {'id': 'moodForm'})
        self.assertIsNotNone(mood_form, "Mood selection form not found")
        
        # Check for mood select
        mood_select = mood_form.find('select', {'name': 'mood'})
        self.assertIsNotNone(mood_select, "Mood select dropdown not found")
        
        # Verify it has options
        options = mood_select.find_all('option')
        self.assertGreater(len(options), 1, "Mood select should have multiple options")
        
    def test_html_validity_basics(self):
        """Test basic HTML validity - proper nesting and structure"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.get_data(as_text=True)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for proper HTML structure
        html_tag = soup.find('html')
        self.assertIsNotNone(html_tag, "HTML tag not found")
        
        head_tag = soup.find('head')
        self.assertIsNotNone(head_tag, "HEAD tag not found")
        
        body_tag = soup.find('body')
        self.assertIsNotNone(body_tag, "BODY tag not found")
        
        # Check for DOCTYPE
        self.assertTrue(html.strip().startswith('<!DOCTYPE html>'), "Missing DOCTYPE declaration")


class TestJavaScriptIntegration(unittest.TestCase):
    """Test JavaScript integration and DOM element matching"""
    
    def test_javascript_dom_element_matching(self):
        """Test that JavaScript looks for correct DOM element IDs"""
        # Read the JavaScript file
        with open('static/script.js', 'r') as f:
            js_content = f.read()
            
        # Get the HTML content
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            soup = BeautifulSoup(html, 'html.parser')
            
        # Check that JavaScript getElementById calls match actual HTML IDs
        js_element_searches = [
            ('search-input', 'playlistSearchInput'),
            ('search-btn', 'searchButton'),
            ('search-results', 'searchResults'),
            ('search-results-list', 'searchResultsList'),
            ('search-loading', 'searchLoading'),
        ]
        
        for html_id, js_var_context in js_element_searches:
            with self.subTest(element_id=html_id):
                # Check HTML has the element
                html_element = soup.find(attrs={'id': html_id})
                self.assertIsNotNone(html_element, f"HTML missing element with id='{html_id}'")
                
                # Check JavaScript references the correct ID
                self.assertIn(f"getElementById('{html_id}')", js_content,
                            f"JavaScript should reference element id='{html_id}'")
                            
    def test_event_listener_targets_exist(self):
        """Test that JavaScript event listeners target existing elements"""
        with open('static/script.js', 'r') as f:
            js_content = f.read()
            
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            soup = BeautifulSoup(html, 'html.parser')
            
        # Common event listener patterns
        if 'addEventListener' in js_content:
            # Check that elements referenced in event listeners exist
            search_btn = soup.find('button', {'id': 'search-btn'})
            self.assertIsNotNone(search_btn, "Search button for event listener not found")
            
            search_input = soup.find('input', {'id': 'search-input'})
            self.assertIsNotNone(search_input, "Search input for event listener not found")


if __name__ == "__main__":
    # Try to import BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        unittest.main(verbosity=2)
    except ImportError:
        print("⚠️  BeautifulSoup4 not available - skipping frontend tests")
        print("   Install with: pip install beautifulsoup4")
        print("   These tests would have caught the search input bug!")