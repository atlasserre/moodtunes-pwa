#!/bin/bash
# Render.com startup script for MoodTunes
echo "Starting MoodTunes PWA..."
gunicorn --bind 0.0.0.0:$PORT app:app