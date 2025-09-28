#!/bin/bash

# Render startup script - ensures app.py is used correctly
echo "🔄 MoodTunes PWA Startup Verification"
echo "====================================="

echo "📍 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo "📁 Available Python files:"
ls -la *.py

echo
echo "🔍 Verifying app.py module..."
if [ -f "app.py" ]; then
    echo "✅ app.py file exists"
    echo "📊 File size: $(stat -c%s app.py) bytes"
    echo "📅 Last modified: $(stat -c%y app.py)"
else
    echo "❌ app.py file not found!"
    exit 1
fi

echo
echo "🧪 Testing module import..."
python -c "
import sys
import os

print('🔍 Python environment:')
print('  Current working directory:', os.getcwd())
print('  Python executable:', sys.executable)
print('  Python path:', sys.path[:3])  # First 3 entries

try:
    print('\\n📦 Importing app module...')
    import app
    print('✅ app module imported successfully')
    
    print('\\n🔍 Checking Flask app...')
    flask_app = app.app
    print('✅ Flask app object found:', type(flask_app))
    print('✅ App name:', flask_app.name)
    print('✅ Debug mode:', flask_app.debug)
    
    print('\\n📋 App version info:')
    version = getattr(app, 'APP_VERSION', 'unknown')
    build_date = getattr(app, 'BUILD_DATE', 'unknown')
    print('✅ Version:', version)
    print('✅ Build date:', build_date)
    
    print('\\n🎯 Testing basic functionality...')
    with flask_app.test_client() as client:
        response = client.get('/')
        print('✅ Home page status:', response.status_code)
        
        # Test version endpoint
        response = client.get('/version')
        if response.status_code == 200:
            version_data = response.get_json()
            print('✅ Version endpoint works:', version_data.get('version'))
        else:
            print('⚠️  Version endpoint status:', response.status_code)
    
    print('\\n🎉 All checks passed - app is ready!')
    
except ImportError as e:
    print('❌ IMPORT ERROR:', e)
    print('\\n🔍 Available files:')
    import os
    for f in os.listdir('.'):
        if f.endswith('.py'):
            print(f'  - {f}')
    exit(1)
except Exception as e:
    print('❌ RUNTIME ERROR:', e)
    import traceback
    traceback.print_exc()
    exit(1)
"

if [ $? -eq 0 ]; then
    echo
    echo "✅ Startup verification successful!"
    echo "🚀 Starting Gunicorn with app:app..."
    exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
else
    echo
    echo "❌ Startup verification failed!"
    exit 1
fi