#!/bin/bash

# Build script for Render deployment
echo "🚀 MoodTunes PWA Build Process"
echo "=============================="

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Verifying app can be imported..."
python -c "from app import app; print('✅ app.py imported successfully')"

echo "🔍 Verifying app structure..."
echo "Main application file: $(ls -la app.py)"
echo "Static files: $(ls -la static/ | wc -l) files"
echo "Templates: $(ls -la templates/ | wc -l) files"

echo "🎉 Build completed successfully!"
echo "🚀 Ready to start with: gunicorn app:app"