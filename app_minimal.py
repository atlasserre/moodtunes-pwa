"""
Minimal version of MoodTunes app for debugging deployment issues
"""
import os
from flask import Flask, render_template, jsonify

# Version information
APP_VERSION = "2.1.1"
BUILD_DATE = "2025-09-28"
BUILD_INFO = {
    "version": APP_VERSION,
    "build_date": BUILD_DATE,
    "features": ["Search", "PWA", "Quality Gates", "88% Coverage", "Version Display"],
    "commit": "latest"
}

# Initialize Flask application
app = Flask(__name__)

@app.route("/")
def index():
    """Main application route with minimal data"""
    template_data = {
        'version_info': BUILD_INFO,
        'mood_categories': {},
        'recent_moods': [],
        'time_suggestions': [],
        'get_mood_info': lambda x: {'name': 'Test', 'icon': '🎵'}
    }
    return render_template("index.html", **template_data)

@app.route("/version")
def version_info():
    """API endpoint to get application version information"""
    return jsonify(BUILD_INFO)

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": APP_VERSION})

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the application
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )