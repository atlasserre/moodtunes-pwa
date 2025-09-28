#!/bin/bash

# 🔍 MoodTunes Deployment Version Checker
# This script helps verify what version is deployed on Render

echo "🔍 MoodTunes Deployment Version Check"
echo "====================================="
echo

# Set the deployment URL
DEPLOY_URL="https://moodtunes-pwa.onrender.com"

echo "📍 Checking deployment at: $DEPLOY_URL"
echo

# Check if the app is responding
echo "1. 🏥 Health Check:"
if curl -s -f "$DEPLOY_URL" > /dev/null; then
    echo "   ✅ App is responding"
else
    echo "   ❌ App is not responding or down"
    exit 1
fi

echo

# Check version endpoint
echo "2. 📋 Version Information:"
VERSION_RESPONSE=$(curl -s "$DEPLOY_URL/version" 2>/dev/null)

if [ $? -eq 0 ] && [ ! -z "$VERSION_RESPONSE" ]; then
    echo "   ✅ Version endpoint available"
    echo "$VERSION_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$VERSION_RESPONSE"
else
    echo "   ❌ Version endpoint not available (older version deployed)"
fi

echo

# Check search functionality
echo "3. 🔍 Search Feature Check:"
SEARCH_RESPONSE=$(curl -s -X POST -d "query=happy" "$DEPLOY_URL/search-playlists" 2>/dev/null)

if echo "$SEARCH_RESPONSE" | grep -q '"success"'; then
    echo "   ✅ Search functionality is available"
    echo "   📊 Search test result:"
    echo "$SEARCH_RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
else
    echo "   ❌ Search functionality not available (older version deployed)"
    echo "   📝 Response: $(echo "$SEARCH_RESPONSE" | head -1)"
fi

echo

# Check basic playlist functionality
echo "4. 🎵 Basic Playlist Check:"
PLAYLIST_RESPONSE=$(curl -s -X POST -d "mood=happy" "$DEPLOY_URL/get-playlist" 2>/dev/null)

if echo "$PLAYLIST_RESPONSE" | grep -q '"playlist"'; then
    echo "   ✅ Basic playlist functionality works"
    echo "   🎵 Test playlist result:"
    echo "$PLAYLIST_RESPONSE" | python3 -m json.tool 2>/dev/null
else
    echo "   ❌ Basic playlist functionality not working"
fi

echo

# Summary
echo "📊 Deployment Summary:"
echo "======================"

# Determine version status
if [ ! -z "$VERSION_RESPONSE" ] && echo "$VERSION_RESPONSE" | grep -q "2.1.0"; then
    echo "✅ Latest version (v2.1.0) is deployed"
    echo "✅ Includes: Search functionality, version display, quality improvements"
elif [ ! -z "$VERSION_RESPONSE" ]; then
    DEPLOYED_VERSION=$(echo "$VERSION_RESPONSE" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('version', 'unknown'))" 2>/dev/null)
    echo "⚠️  Version $DEPLOYED_VERSION is deployed (not latest 2.1.0)"
else
    echo "⚠️  Older version deployed (no version endpoint available)"
fi

# Check if search is available
if echo "$SEARCH_RESPONSE" | grep -q '"success"'; then
    echo "✅ Search feature is functional"
else
    echo "❌ Search feature is missing"
fi

echo
echo "🚀 To force redeploy latest version:"
echo "   1. Go to https://dashboard.render.com"
echo "   2. Find your moodtunes-pwa service"
echo "   3. Click 'Manual Deploy' → 'Deploy latest commit'"
echo "   4. Wait for deployment to complete"
echo "   5. Run this script again to verify"

echo