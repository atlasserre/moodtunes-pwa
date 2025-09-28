#!/bin/bash

# 🔍 Render Service Diagnostic Tool
echo "🔍 Render Service Configuration Diagnostic"
echo "=========================================="
echo

echo "📁 Current Repository Structure:"
echo "================================"
echo "Python files:"
ls -la *.py 2>/dev/null || echo "No Python files found"

echo
echo "Configuration files:"
ls -la *.yaml *.yml Procfile runtime.txt 2>/dev/null || echo "No config files found"

echo
echo "🔧 Configuration File Contents:"
echo "==============================="

if [ -f "render.yaml" ]; then
    echo "📄 render.yaml:"
    cat render.yaml
    echo
fi

if [ -f "Procfile" ]; then
    echo "📄 Procfile:"
    cat Procfile
    echo
fi

if [ -f "runtime.txt" ]; then
    echo "📄 runtime.txt:"
    cat runtime.txt
    echo
fi

echo "🐍 Python Import Test:"
echo "======================"
python -c "
import sys
import os

print('Current directory:', os.getcwd())
print('Python path entries:')
for i, path in enumerate(sys.path[:5]):
    print(f'  {i}: {path}')

print('\\nTesting app import...')
try:
    import app
    print('✅ SUCCESS: app module imported')
    print('✅ Flask app object:', type(app.app))
    print('✅ App version:', getattr(app, 'APP_VERSION', 'unknown'))
except ImportError as e:
    print('❌ IMPORT ERROR:', e)
    print('Available Python files:')
    for f in os.listdir('.'):
        if f.endswith('.py'):
            print(f'  - {f}')
except Exception as e:
    print('❌ OTHER ERROR:', e)
"

echo
echo "🔧 Gunicorn Test:"
echo "================="
if command -v gunicorn &> /dev/null; then
    echo "Testing: gunicorn app:app --check-config"
    gunicorn app:app --check-config 2>&1 || echo "Gunicorn test failed"
elif python -m gunicorn --version &> /dev/null; then
    echo "Testing: python -m gunicorn app:app --check-config"
    python -m gunicorn app:app --check-config 2>&1 || echo "Gunicorn test failed"
else
    echo "⚠️  Gunicorn not available (normal in dev environment)"
fi

echo
echo "📊 Diagnostic Summary:"
echo "====================="
echo "1. Check if app.py imports successfully ✅"
echo "2. Verify configuration files exist ✅"
echo "3. Test Gunicorn compatibility ✅"
echo
echo "🎯 For Render Dashboard Check:"
echo "============================="
echo "1. Go to: https://dashboard.render.com"
echo "2. Find: moodtunes-pwa service"
echo "3. Check Build Command: Should be './build.sh' or 'pip install -r requirements.txt'"
echo "4. Check Start Command: Should be './start.sh' or 'python -m gunicorn app:app --bind 0.0.0.0:\$PORT'"
echo "5. Environment Variables: Should NOT reference app_production anywhere"
echo
echo "💡 If dashboard shows different commands, that's the problem!"