#!/bin/bash

# Build script for Render deployment
echo "🚀 MoodTunes PWA Build Process"
echo "=============================="

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔍 Verifying Python environment..."
python --version
which python

echo "📁 Checking file structure..."
echo "Current directory: $(pwd)"
echo "Files in root:"
ls -la *.py

echo "✅ Testing app import..."
python -c "
import sys
print('Python path:', sys.path)
print('Current directory contents:', $(ls -la))

try:
    import app
    print('✅ app module imported successfully')
    print('✅ Flask app object:', type(app.app))
    print('✅ App version:', getattr(app, 'APP_VERSION', 'unknown'))
except ImportError as e:
    print('❌ Failed to import app module:', e)
    import traceback
    traceback.print_exc()
    exit(1)
except Exception as e:
    print('❌ Error with app module:', e)
    import traceback
    traceback.print_exc()
    exit(1)
"

echo "🔧 Verifying Gunicorn can find the app..."
python -c "
try:
    from app import app as flask_app
    print('✅ Gunicorn target app:app is accessible')
    print('✅ Flask app name:', flask_app.name)
    print('✅ Flask app config:', dict(flask_app.config))
except Exception as e:
    print('❌ Gunicorn target app:app failed:', e)
    exit(1)
"

echo "🔍 Environment check..."
echo "FLASK_ENV: ${FLASK_ENV:-not set}"
echo "PORT: ${PORT:-not set}"

echo "🎉 Build completed successfully!"
echo "🚀 Ready to start with: gunicorn app:app"