
import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Mood to playlist mapping
mood_playlists = {
    # Original moods
    "happy": "37i9dQZF1DX0XUsuxWHRQd",  # Happy Hits
    "sad": "37i9dQZF1DX7qK8ma5wgG1",   # Sad Songs
    "energetic": "37i9dQZF1DX76Wlfdnj7AP",  # Beast Mode
    "chill": "37i9dQZF1DWVqfgj8NZEp1",  # Lofi Chill
    "romantic": "37i9dQZF1DX50QitC6Oqtn",  # Love Pop
    
    # New mood additions
    "motivated": "37i9dQZF1DX0XUfTFmNdCA",  # Beast Mode (alternative workout)
    "sleepy": "37i9dQZF1DWZd79rJ6a7lp",   # Sleep
    "focused": "37i9dQZF1DWZeKCadgRdKQ",  # Deep Focus
    "party": "37i9dQZF1DXdPec7aLTmlC",    # Pop Rising
    "nostalgic": "37i9dQZF1DX4o1oenSJRJd",  # All Out 2010s
    "angry": "37i9dQZF1DX9qNs32fujYe",    # Heavy Metal
    "melancholy": "37i9dQZF1DX59NCqCqJtoH",  # Atmospheric Calm
    "uplifting": "37i9dQZF1DX6GwdWRQMQpq",  # Good Vibes
    "meditative": "37i9dQZF1DWZqd5JICZI0u",  # Peaceful Piano
    "running": "37i9dQZF1DWUa8ZRTfalHk"   # Power Workout
}

# Mood categories for organized display
mood_categories = {
    "Emotional": {
        "moods": ["happy", "sad", "romantic", "angry", "melancholy", "uplifting", "nostalgic"],
        "icon": "😊",
        "description": "Express your feelings"
    },
    "Energy & Activity": {
        "moods": ["energetic", "motivated", "party", "running", "chill"],
        "icon": "⚡",
        "description": "Match your energy level"
    },
    "Mental State": {
        "moods": ["focused", "meditative", "sleepy"],
        "icon": "🧠",
        "description": "Support your mindset"
    }
}

# Time-based mood suggestions
def get_time_based_suggestions():
    """Get mood suggestions based on current time of day"""
    current_hour = datetime.now().hour
    
    if 6 <= current_hour < 9:  # Morning (6AM-9AM)
        return ["uplifting", "motivated", "energetic"]
    elif 9 <= current_hour < 12:  # Late Morning (9AM-12PM)
        return ["focused", "motivated", "happy"]
    elif 12 <= current_hour < 14:  # Lunch (12PM-2PM)
        return ["chill", "happy", "uplifting"]
    elif 14 <= current_hour < 17:  # Afternoon (2PM-5PM)
        return ["focused", "energetic", "motivated"]
    elif 17 <= current_hour < 20:  # Evening (5PM-8PM)
        return ["chill", "happy", "party"]
    elif 20 <= current_hour < 22:  # Night (8PM-10PM)
        return ["romantic", "chill", "nostalgic"]
    else:  # Late Night (10PM-6AM)
        return ["sleepy", "meditative", "chill"]

def get_mood_display_info(mood_key):
    """Get display information for a mood"""
    mood_icons = {
        "happy": "😊", "sad": "😢", "energetic": "💪", "chill": "😌", "romantic": "❤️",
        "motivated": "🔥", "sleepy": "😴", "focused": "🤔", "party": "🎉", "nostalgic": "😌",
        "angry": "😠", "melancholy": "🌧️", "uplifting": "☀️", "meditative": "🧘", "running": "🏃"
    }
    
    mood_names = {
        "happy": "Happy", "sad": "Sad", "energetic": "Energetic", "chill": "Chill", "romantic": "Romantic",
        "motivated": "Motivated", "sleepy": "Sleepy", "focused": "Focused", "party": "Party", "nostalgic": "Nostalgic",
        "angry": "Angry", "melancholy": "Melancholy", "uplifting": "Uplifting", "meditative": "Meditative", "running": "Running"
    }
    
    return {
        "key": mood_key,
        "name": mood_names.get(mood_key, mood_key.title()),
        "icon": mood_icons.get(mood_key, "🎵")
    }

@app.route("/")
def index():
    # Get recent moods from session (last 3)
    recent_moods = session.get('recent_moods', [])
    
    # Get time-based suggestions
    time_suggestions = get_time_based_suggestions()
    
    # Prepare data for template
    template_data = {
        'mood_categories': mood_categories,
        'recent_moods': [get_mood_display_info(mood) for mood in recent_moods[-3:]],
        'time_suggestions': [get_mood_display_info(mood) for mood in time_suggestions],
        'get_mood_info': get_mood_display_info
    }
    
    return render_template("index.html", **template_data)

@app.route("/get-playlist", methods=["POST"])
def get_playlist():
    try:
        # Get and validate mood input
        mood = request.form.get("mood", "").strip().lower()
        
        if not mood:
            app.logger.warning("Empty mood parameter received")
            return jsonify({"error": "Mood is required"}), 400
            
        if mood not in mood_playlists:
            app.logger.warning(f"Invalid mood requested: {mood}")
            return jsonify({"error": "Invalid mood selected"}), 400
        
        playlist_id = mood_playlists.get(mood)
        embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator&theme=0"
        web_url = f"https://open.spotify.com/playlist/{playlist_id}"
        
        # Track recent moods in session
        recent_moods = session.get('recent_moods', [])
        if mood in recent_moods:
            recent_moods.remove(mood)  # Remove if already exists
        recent_moods.append(mood)  # Add to end
        session['recent_moods'] = recent_moods[-5:]  # Keep last 5 moods
        
        app.logger.info(f"Successfully served playlist for mood: {mood}")
        return jsonify({
            "playlist": web_url,
            "embed_url": embed_url,
            "mood": mood
        })
        
    except Exception as e:
        app.logger.error(f"Error in get_playlist: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/static/service-worker.js')
def service_worker():
    """Serve service worker with proper headers"""
    from flask import send_from_directory
    response = send_from_directory('static', 'service-worker.js')
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

if __name__ == "__main__":
    # Use debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)