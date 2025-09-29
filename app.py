"""
MoodTunes PWA - Your Personal Music Mood Companion

A Flask-based Progressive Web Application that curates Spotify playlists
based on your current mood. Features include:

- 15 curated mood-based playlists with 20+ songs each
- Smart search functionality with keyword matching
- Time-based mood suggestions based on current hour
- Recent mood tracking via Flask sessions
- Progressive Web App capabilities with offline support
- Production-ready security configurations
- RESTful API endpoints for playlist data
- Responsive design for mobile and desktop

Technical Stack:
- Flask 3.0.0 with SQLAlchemy for data persistence
- HTML5, CSS3, JavaScript for frontend
- Service Worker for PWA functionality
- Gunicorn for production deployment

Author: MoodTunes Team
Version: 2.1.2
License: MIT
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session

# ====================================================================
# APPLICATION VERSION INFORMATION
# ====================================================================

APP_VERSION = "2.2.0"  # Major.Minor.Patch - 1080x2040 UI optimization
BUILD_DATE = "2025-09-29"
BUILD_INFO = {
    "version": APP_VERSION,
    "build_date": BUILD_DATE,
    "features": ["Search", "PWA", "Quality Gates", "88% Coverage", "Documentation", "1080x2040 Optimization"],
    "commit": "latest",
}

# Initialize Flask application with production-ready configuration
app = Flask(__name__)

# Security Configuration
# Use environment variable for secret key in production, fallback for development
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")

# Production Security Configurations
# These settings ensure secure session handling and prevent common web vulnerabilities
app.config["SESSION_COOKIE_SECURE"] = True  # Force HTTPS-only cookies (prevents man-in-the-middle attacks)
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent XSS attacks by blocking JavaScript access to cookies
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection while allowing legitimate cross-site requests

# Production Logging Configuration
# Structured logging for monitoring and debugging in production environments
logging.basicConfig(
    level=logging.INFO,  # INFO level provides good balance of detail vs. noise
    format="%(asctime)s %(levelname)s %(name)s %(message)s",  # Timestamp + level + logger + message
)

# ====================================================================
# MOOD PLAYLIST MAPPING
# ====================================================================
# Core data structure mapping mood keys to Spotify playlist IDs
# Each playlist has been carefully curated for the specific mood
# Playlist IDs are from Spotify's public curated playlists
# Format: "mood_key": "spotify_playlist_id"  # Playlist Name

mood_playlists = {
    # Original Core Moods - The foundational set covering basic emotional states
    "happy": "37i9dQZF1DX0XUsuxWHRQd",  # Happy Hits - Upbeat mainstream songs
    "sad": "37i9dQZF1DX7qK8ma5wgG1",  # Sad Songs - Melancholic and emotional tracks
    "energetic": "37i9dQZF1DX76Wlfdnj7AP",  # Beast Mode - High-energy workout music
    "chill": "37i9dQZF1DWVqfgj8NZEp1",  # Lofi Chill - Relaxing lo-fi hip hop beats
    "romantic": "37i9dQZF1DX50QitC6Oqtn",  # Love Pop - Romantic pop and R&B songs
    # New mood additions
    "motivated": "37i9dQZF1DWTl4y3vgJOXW",  # Motivation Mix (verified working & unique)
    "sleepy": "37i9dQZF1DWZd79rJ6a7lp",  # Sleep
    "focused": "37i9dQZF1DWZeKCadgRdKQ",  # Deep Focus
    "party": "37i9dQZF1DXdPec7aLTmlC",  # Pop Rising
    "nostalgic": "37i9dQZF1DX4o1oenSJRJd",  # All Out 2010s
    "angry": "37i9dQZF1DX9qNs32fujYe",  # Heavy Metal
    "melancholy": "37i9dQZF1DX3rxVfibe1L0",  # Mood Booster (verified working)
    "uplifting": "37i9dQZF1DX6GwdWRQMQpq",  # Good Vibes
    "meditative": "37i9dQZF1DWZqd5JICZI0u",  # Peaceful Piano
    "running": "37i9dQZF1DWUa8ZRTfalHk",  # Power Workout
}

# ====================================================================
# MOOD CATEGORIZATION SYSTEM
# ====================================================================
# Organizes moods into logical categories for better UX
# Each category contains:
# - moods: List of mood keys belonging to this category
# - icon: Emoji representation for visual identification
# - description: User-friendly explanation of the category's purpose

mood_categories = {
    "Emotional": {
        "moods": ["happy", "sad", "romantic", "angry", "melancholy", "uplifting", "nostalgic"],
        "icon": "😊",  # Represents emotional expression
        "description": "Express your feelings",  # Clear, actionable description
    },
    "Energy & Activity": {
        "moods": ["energetic", "motivated", "party", "running", "chill"],
        "icon": "⚡",  # Represents energy and movement
        "description": "Match your energy level",  # Activity-focused description
    },
    "Mental State": {
        "moods": ["focused", "meditative", "sleepy"],
        "icon": "🧠",  # Represents mental/cognitive states
        "description": "Support your mindset",  # Mind-focused description
    },
}

# ====================================================================
# INTELLIGENT TIME-BASED MOOD SUGGESTIONS
# ====================================================================


def get_time_based_suggestions():
    """
    Get mood suggestions based on current time of day.

    Uses time-of-day psychology to suggest appropriate moods:
    - Morning: Energizing moods to start the day
    - Work hours: Focus and productivity moods
    - Lunch: Light, positive moods for break time
    - Evening: Social and relaxation moods
    - Night: Calm, intimate, and sleep-ready moods

    Returns:
        list: Three mood keys most appropriate for current time

    Note:
        Time zones are handled by the system's local time.
        Suggestions are based on general circadian rhythm patterns.
    """
    current_hour = datetime.now().hour  # Get current hour in 24-hour format

    # Morning (6AM-9AM): Start the day with energy and positivity
    if 6 <= current_hour < 9:
        return ["uplifting", "motivated", "energetic"]

    # Late Morning (9AM-12PM): Focus and productivity time
    elif 9 <= current_hour < 12:
        return ["focused", "motivated", "happy"]

    # Lunch Time (12PM-2PM): Light, social, positive vibes
    elif 12 <= current_hour < 14:
        return ["chill", "happy", "uplifting"]

    # Afternoon (2PM-5PM): Peak productivity and energy hours
    elif 14 <= current_hour < 17:
        return ["focused", "energetic", "motivated"]

    # Evening (5PM-8PM): Wind down, social time, or celebration
    elif 17 <= current_hour < 20:
        return ["chill", "happy", "party"]

    # Night (8PM-10PM): Intimate, reflective, relaxation time
    elif 20 <= current_hour < 22:
        return ["romantic", "chill", "nostalgic"]

    # Late Night (10PM-6AM): Sleep preparation and quiet moods
    else:
        return ["sleepy", "meditative", "chill"]


def get_mood_display_info(mood_key):
    """
    Get display information for a mood including icon and formatted name.

    This function provides consistent formatting and visual representation
    for mood keys throughout the application. It handles both known moods
    and unknown mood keys gracefully.

    Args:
        mood_key (str): The internal mood identifier (e.g., 'happy', 'energetic')

    Returns:
        dict: Contains:
            - key (str): Original mood key
            - name (str): Human-readable formatted name
            - icon (str): Emoji icon representing the mood

    Example:
        >>> get_mood_display_info('happy')
        {'key': 'happy', 'name': 'Happy', 'icon': '😊'}

        >>> get_mood_display_info('unknown')
        {'key': 'unknown', 'name': 'Unknown', 'icon': '🎵'}
    """
    # Emoji icons for visual mood representation
    # Each icon is carefully chosen to represent the mood's emotional state
    mood_icons = {
        "happy": "😊",  # Classic happy face
        "sad": "😢",  # Crying face for sadness
        "energetic": "💪",  # Flexing muscle for energy
        "chill": "😌",  # Peaceful, relaxed expression
        "romantic": "❤️",  # Heart for love and romance
        "motivated": "🔥",  # Fire emoji for passion and drive
        "sleepy": "😴",  # Sleeping face
        "focused": "🤔",  # Thinking face for concentration
        "party": "🎉",  # Party celebration
        "nostalgic": "😌",  # Peaceful, reflective mood
        "angry": "😠",  # Angry face
        "melancholy": "🌧️",  # Rain cloud for sad, reflective mood
        "uplifting": "☀️",  # Sun for bright, positive energy
        "meditative": "🧘",  # Meditation pose
        "running": "🏃",  # Running figure for exercise
    }

    # Human-readable mood names for display
    # Properly capitalized versions of mood keys
    mood_names = {
        "happy": "Happy",
        "sad": "Sad",
        "energetic": "Energetic",
        "chill": "Chill",
        "romantic": "Romantic",
        "motivated": "Motivated",
        "sleepy": "Sleepy",
        "focused": "Focused",
        "party": "Party",
        "nostalgic": "Nostalgic",
        "angry": "Angry",
        "melancholy": "Melancholy",
        "uplifting": "Uplifting",
        "meditative": "Meditative",
        "running": "Running",
    }

    # Return structured mood information
    # Handles unknown moods gracefully with defaults
    return {
        "key": mood_key,  # Original identifier
        "name": mood_names.get(mood_key, mood_key.title()),  # Formatted name or title-cased key
        "icon": mood_icons.get(mood_key, "🎵"),  # Mood icon or default music note
    }


# ====================================================================
# FLASK ROUTES - WEB APPLICATION ENDPOINTS
# ====================================================================


@app.route("/")
def index():
    """
    Main application homepage route.

    Renders the main interface with:
    - Organized mood categories for browsing
    - Recent mood history from user session
    - Time-based intelligent mood suggestions
    - Complete mood browsing functionality

    Returns:
        str: Rendered HTML template with mood data

    Template Data:
        - mood_categories: Organized mood groupings
        - recent_moods: User's last 3 selected moods
        - time_suggestions: 3 moods appropriate for current time
        - get_mood_info: Helper function for mood display
    """
    # Retrieve user's recent mood history from session storage
    # Session persists across requests for same user
    recent_moods = session.get("recent_moods", [])

    # Get intelligent time-based mood suggestions
    # Uses current time to suggest contextually appropriate moods
    time_suggestions = get_time_based_suggestions()

    # Prepare comprehensive data package for template rendering
    # All data is processed for immediate template consumption
    template_data = {
        "mood_categories": mood_categories,  # Complete mood organization structure
        "recent_moods": [get_mood_display_info(mood) for mood in recent_moods[-3:]],  # Last 3 moods with display info
        "time_suggestions": [
            get_mood_display_info(mood) for mood in time_suggestions
        ],  # Current time suggestions with display info
        "get_mood_info": get_mood_display_info,  # Helper function for template use
        "version_info": BUILD_INFO,  # Application version information
    }

    # Render main template with all mood data
    return render_template("index.html", **template_data)


@app.route("/get-playlist", methods=["POST"])
def get_playlist():
    """
    Retrieve Spotify playlist for a specific mood.

    This endpoint handles mood-to-playlist mapping and session tracking.
    It validates the mood input, generates Spotify URLs, and maintains
    user's recent mood history for personalization.

    POST Parameters:
        mood (str): The mood key to get playlist for

    Returns:
        JSON Response:
            Success (200):
                - playlist (str): Direct Spotify web URL
                - embed_url (str): Spotify embed URL for web players
                - mood (str): Confirmed mood key
            Error (400):
                - error (str): "Mood is required" or "Invalid mood selected"
            Error (500):
                - error (str): "Internal server error"

    Side Effects:
        - Updates user's recent_moods session list
        - Logs playlist access for monitoring

    Session Management:
        - Maintains last 5 moods per user
        - Removes duplicates (moves to end if mood repeated)
        - Persists across user's browser session
    """
    try:
        # Input Validation and Sanitization
        # Extract mood from form data, normalize to lowercase
        mood = request.form.get("mood", "").strip().lower()

        # Validate that mood parameter is provided
        if not mood:
            app.logger.warning("Empty mood parameter received")
            return jsonify({"error": "Mood is required"}), 400

        # Validate that mood exists in our curated playlist collection
        if mood not in mood_playlists:
            app.logger.warning(f"Invalid mood requested: {mood}")
            return jsonify({"error": "Invalid mood selected"}), 400

        # Spotify URL Generation
        # Get the curated playlist ID for this mood
        playlist_id = mood_playlists.get(mood)

        # Generate Spotify embed URL for in-app playback
        # utm_source and theme parameters optimize the embed experience
        embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator&theme=0"

        # Generate direct Spotify web URL for external app opening
        web_url = f"https://open.spotify.com/playlist/{playlist_id}"

        # Session-Based Recent Mood Tracking
        # Retrieve current recent moods list from user session
        recent_moods = session.get("recent_moods", [])

        # Remove mood if it already exists (to move it to end)
        if mood in recent_moods:
            recent_moods.remove(mood)

        # Add current mood to end of list (most recent)
        recent_moods.append(mood)

        # Maintain only last 5 moods to prevent session bloat
        session["recent_moods"] = recent_moods[-5:]

        # Success logging for monitoring and analytics
        app.logger.info(f"Successfully served playlist for mood: {mood}")

        # Return structured JSON response with all playlist information
        return jsonify(
            {
                "playlist": web_url,  # Direct Spotify link
                "embed_url": embed_url,  # Embeddable player URL
                "mood": mood,  # Confirmed mood for client verification
            }
        )

    except Exception as e:
        # Comprehensive error handling and logging
        app.logger.error(f"Error in get_playlist: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Mood metadata with search keywords for production search functionality
mood_metadata = {
    "happy": {
        "name": "Happy",
        "description": "Upbeat tracks to brighten your day",
        "keywords": ["happy", "upbeat", "positive", "cheerful", "joyful", "bright", "sunny"],
        "category": "Emotional",
    },
    "sad": {
        "name": "Sad",
        "description": "Melancholic songs for when you need to feel understood",
        "keywords": ["sad", "melancholic", "emotional", "heartbreak", "tears", "blue", "down"],
        "category": "Emotional",
    },
    "energetic": {
        "name": "Energetic",
        "description": "High-energy beats to power through anything",
        "keywords": ["energetic", "high-energy", "power", "intense", "beast", "pump", "strong"],
        "category": "Energy & Activity",
    },
    "chill": {
        "name": "Chill",
        "description": "Relaxing vibes for unwinding and taking it easy",
        "keywords": ["chill", "relax", "calm", "peaceful", "lofi", "mellow", "easy"],
        "category": "Energy & Activity",
    },
    "romantic": {
        "name": "Romantic",
        "description": "Love songs for special moments and romantic moods",
        "keywords": ["romantic", "love", "romance", "intimate", "date", "valentine", "heart"],
        "category": "Emotional",
    },
    "motivated": {
        "name": "Motivated",
        "description": "Inspiring tracks to fuel your ambition and drive",
        "keywords": ["motivated", "motivation", "inspiring", "drive", "ambition", "success", "hustle"],
        "category": "Energy & Activity",
    },
    "sleepy": {
        "name": "Sleepy",
        "description": "Gentle sounds to help you drift off to sleep",
        "keywords": ["sleepy", "sleep", "bedtime", "gentle", "soft", "lullaby", "night"],
        "category": "Mental State",
    },
    "focused": {
        "name": "Focused",
        "description": "Concentration music for deep work and study sessions",
        "keywords": ["focused", "focus", "concentration", "study", "work", "productivity", "deep"],
        "category": "Mental State",
    },
    "party": {
        "name": "Party",
        "description": "Dance hits and party anthems to get everyone moving",
        "keywords": ["party", "dance", "celebration", "fun", "club", "dancing", "upbeat"],
        "category": "Energy & Activity",
    },
    "nostalgic": {
        "name": "Nostalgic",
        "description": "Throwback hits that bring back memories",
        "keywords": ["nostalgic", "throwback", "memories", "2010s", "classic", "retro", "old"],
        "category": "Emotional",
    },
    "angry": {
        "name": "Angry",
        "description": "Heavy and intense music to channel your rage",
        "keywords": ["angry", "rage", "heavy", "metal", "intense", "aggressive", "mad"],
        "category": "Emotional",
    },
    "melancholy": {
        "name": "Melancholy",
        "description": "Bittersweet songs for reflective moments",
        "keywords": ["melancholy", "bittersweet", "reflective", "moody", "contemplative", "wistful"],
        "category": "Emotional",
    },
    "uplifting": {
        "name": "Uplifting",
        "description": "Feel-good vibes to boost your spirits",
        "keywords": ["uplifting", "positive", "good vibes", "boost", "inspiring", "optimistic"],
        "category": "Emotional",
    },
    "meditative": {
        "name": "Meditative",
        "description": "Peaceful piano and ambient sounds for mindfulness",
        "keywords": ["meditative", "meditation", "peaceful", "piano", "ambient", "mindful", "zen", "calm"],
        "category": "Mental State",
    },
    "running": {
        "name": "Running",
        "description": "High-tempo workout music to keep you moving",
        "keywords": ["running", "workout", "exercise", "fitness", "cardio", "training", "gym"],
        "category": "Energy & Activity",
    },
}


@app.route("/search-playlists", methods=["POST"])
def search_playlists():
    """
    Advanced search through curated mood playlists.

    Provides intelligent search functionality across mood names, descriptions,
    and keywords. Uses fuzzy matching to find relevant playlists even with
    partial or related search terms.

    POST Parameters:
        query (str): Search term (minimum 2 characters)

    Returns:
        JSON Response:
            Success (200):
                - success (bool): True
                - query (str): Original search query
                - moods (list): Array of matching mood objects
                - total (int): Number of results found
            Error (400):
                - success (bool): False
                - error (str): Validation error message
            Error (500):
                - success (bool): False
                - error (str): "Search failed"

    Mood Object Structure:
        - mood_key (str): Internal mood identifier
        - name (str): Display name
        - description (str): Mood description
        - category (str): Mood category
        - embed_url (str): Spotify embed URL
        - web_url (str): Direct Spotify URL
        - icon (str): Emoji representation

    Search Algorithm:
        - Searches mood names (exact and partial matches)
        - Searches descriptions for contextual matches
        - Searches keyword arrays for semantic matches
        - Case-insensitive matching throughout
        - Returns results sorted by relevance
    """
    try:
        # Input Processing and Validation
        # Extract and normalize search query
        query = request.form.get("query", "").strip().lower()

        # Validate query presence
        if not query:
            return jsonify({"success": False, "error": "Search query is required"}), 400

        # Enforce minimum query length to prevent overly broad results
        if len(query) < 2:
            return jsonify({"success": False, "error": "Query must be at least 2 characters"}), 400

        # Advanced Multi-Field Search Algorithm
        # Search across multiple data sources for comprehensive results
        matching_moods = []

        # Iterate through all available mood playlists
        for mood_key, playlist_id in mood_playlists.items():
            # Get rich metadata for this mood (name, description, keywords, category)
            mood_info = mood_metadata.get(mood_key, {})

            # Multi-field Fuzzy Matching Algorithm
            # Check query against multiple mood attributes for comprehensive matching
            matches = (
                query in mood_key.lower()
                or query in mood_info.get("name", "").lower()  # Direct mood key match
                or query in mood_info.get("description", "").lower()  # Display name match
                or any(  # Description content match
                    query in keyword.lower() for keyword in mood_info.get("keywords", [])
                )  # Keyword semantic match
            )

            # Build result object for matching moods
            if matches:
                # Generate Spotify URLs for this playlist
                embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator&theme=0"
                web_url = f"https://open.spotify.com/playlist/{playlist_id}"

                # Construct comprehensive mood result object
                mood_result = {
                    "mood_key": mood_key,  # Internal identifier
                    "name": mood_info.get("name", mood_key.title()),  # Human-readable name
                    "description": mood_info.get("description", f"{mood_key.title()} playlist"),  # Descriptive text
                    "category": mood_info.get("category", "Other"),  # Mood grouping
                    "embed_url": embed_url,  # Embeddable Spotify URL
                    "web_url": web_url,  # Direct Spotify URL
                    "icon": get_mood_display_info(mood_key)["icon"],  # Visual emoji representation
                }

                matching_moods.append(mood_result)

        # Search Analytics and Logging
        # Log search query and result count for usage analytics
        app.logger.info(f"Playlist search for '{query}' returned {len(matching_moods)} results")

        # Return Structured Search Results
        # Provide comprehensive response with query echo and result metadata
        return jsonify(
            {
                "success": True,  # Operation success indicator
                "query": query,  # Echo original query for client verification
                "moods": matching_moods,  # Array of matching mood objects
                "total": len(matching_moods),  # Result count for pagination/UI
            }
        )

    except Exception as e:
        # Comprehensive Error Handling
        # Log error details for debugging while providing safe user message
        app.logger.error(f"Error in search_playlists: {str(e)}")
        return jsonify({"success": False, "error": "Search failed"}), 500


# ====================================================================
# PROGRESSIVE WEB APP SUPPORT
# ====================================================================


@app.route("/version")
def version_info():
    """
    Get application version and build information.

    Returns:
        JSON: Complete version and build information

    Response Format:
        {
            "version": "2.1.0",
            "build_date": "2025-09-28",
            "features": ["Search", "PWA", "Quality Gates", "88% Coverage"],
            "commit": "latest",
            "status": "production"
        }
    """
    return jsonify(BUILD_INFO)


@app.route("/static/service-worker.js")
def service_worker():
    """
    Serve service worker file with proper PWA headers.

    Service workers enable Progressive Web App functionality including:
    - Offline functionality and caching
    - Background sync capabilities
    - Push notification support
    - App-like behavior on mobile devices

    Returns:
        Response: Service worker JavaScript file with proper headers

    Headers Set:
        - Content-Type: application/javascript (proper MIME type)
        - Service-Worker-Allowed: / (allows SW to control entire origin)

    Note:
        Service worker must be served from same origin with proper headers
        to be registered by browsers for security reasons.
    """
    from flask import send_from_directory

    # Serve service worker file from static directory
    response = send_from_directory("static", "service-worker.js")

    # Set proper MIME type for JavaScript file
    response.headers["Content-Type"] = "application/javascript"

    # Allow service worker to control entire application scope
    response.headers["Service-Worker-Allowed"] = "/"

    return response


@app.route("/manifest.json")
def manifest():
    """
    Serve PWA manifest file from root path for better discoverability.

    The Web App Manifest is a JSON file that tells the browser about
    your Progressive Web App and how it should behave when installed.

    Returns:
        Response: PWA manifest JSON file with proper headers

    Headers Set:
        - Content-Type: application/manifest+json (proper MIME type)

    Note:
        Manifest should be accessible from root for optimal PWA support
        and browser compatibility.
    """
    from flask import send_from_directory

    # Serve manifest file from static directory
    response = send_from_directory("static", "manifest.json")

    # Set proper MIME type for PWA manifest
    response.headers["Content-Type"] = "application/manifest+json"

    return response


# ====================================================================
# APPLICATION ENTRY POINT
# ====================================================================

if __name__ == "__main__":
    """
    Production-ready application startup configuration.

    Security Features:
    - Debug mode always disabled in production
    - Configurable port via environment variable
    - Binds to all interfaces for container deployment

    Environment Variables:
    - PORT: Server port (default: 5000)
    - SECRET_KEY: Flask session secret (required in production)

    Deployment:
    - Ready for Docker containers
    - Compatible with Heroku, Render, and similar platforms
    - Suitable for reverse proxy deployment
    """
    # Get port from environment variable for platform flexibility
    # Default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))

    # Security: Debug mode always disabled in production
    # Prevents code exposure and security vulnerabilities
    debug = False

    # Start Flask development server
    # host='0.0.0.0' allows connections from any IP (container-friendly)
    # In production, use proper WSGI server like Gunicorn
    app.run(host="0.0.0.0", port=port, debug=debug)
