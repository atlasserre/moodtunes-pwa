#!/bin/bash

# Emergency deployment script to fix version display
echo "🔧 Starting emergency deployment fix..."

# Test minimal app first
echo "📋 Testing minimal app..."
python app_minimal.py &
MINIMAL_PID=$!
sleep 3

# Test if minimal app works
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ Minimal app works - issue is in main app"
    kill $MINIMAL_PID
else
    echo "❌ Even minimal app fails - deeper issue"
    kill $MINIMAL_PID
    exit 1
fi

# Check main app imports
echo "📋 Testing main app imports..."
python -c "
try:
    from app import app, BUILD_INFO
    print('✅ Main app imports successfully')
    print(f'✅ Version info: {BUILD_INFO}')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Test if main app can start
echo "📋 Testing main app startup..."
timeout 10 python app.py &
MAIN_PID=$!
sleep 5

if curl -s http://localhost:5000/version > /dev/null; then
    echo "✅ Main app starts and responds"
    kill $MAIN_PID
else
    echo "❌ Main app fails to start or respond"
    kill $MAIN_PID 2>/dev/null
fi

echo "🎯 Deployment diagnosis complete!"