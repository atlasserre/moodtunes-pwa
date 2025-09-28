#!/bin/bash

# 🚨 Emergency Render Deployment Fix
# This script completely eliminates any app_production references

echo "🚨 Emergency Deployment Fix for Render"
echo "======================================"

echo "🔍 Checking for app_production references..."

# Remove any potential app_production files
if [ -f "app_production.py" ]; then
    echo "🗑️  Removing old app_production.py file"
    rm -f app_production.py
fi

if [ -f "app_production.pyc" ]; then
    echo "🗑️  Removing compiled app_production.pyc"
    rm -f app_production.pyc
fi

# Clear any Python cache
echo "🧹 Clearing Python cache..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

echo "✅ Verifying app.py is the only main file..."
python -c "
import os
import sys

# Ensure app.py exists and is importable
if not os.path.exists('app.py'):
    print('❌ app.py not found!')
    sys.exit(1)

print('✅ app.py exists')

# Test import
try:
    import app
    print('✅ app module imports successfully')
    print('✅ Flask app available:', hasattr(app, 'app'))
    print('✅ Version:', getattr(app, 'APP_VERSION', 'unknown'))
except Exception as e:
    print('❌ Import failed:', e)
    sys.exit(1)
"

# Verify Gunicorn command
echo "🔧 Testing Gunicorn command..."
python -m gunicorn --check-config app:app
if [ $? -eq 0 ]; then
    echo "✅ Gunicorn configuration valid"
else
    echo "❌ Gunicorn configuration invalid"
    exit 1
fi

echo "🚀 Emergency fix complete!"
echo "📝 Summary:"
echo "  - Removed any app_production files"
echo "  - Cleared Python cache"
echo "  - Verified app.py imports correctly"
echo "  - Confirmed Gunicorn can use app:app"
echo
echo "🎯 Deploy with confidence using: gunicorn app:app"