#!/bin/bash

# 📊 GitHub Actions Pipeline Monitor
# This script helps track the current pipeline execution

echo "📊 MoodTunes CI/CD Pipeline Monitor"
echo "===================================="
echo

# Repository information
REPO="atlasserre/moodtunes-pwa"
BRANCH="main"

echo "📍 Repository: $REPO"
echo "🌿 Branch: $BRANCH"
echo "🕐 Check Time: $(date)"
echo

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "🔍 Latest Pipeline Runs:"
    echo "========================"
    
    # Get recent workflow runs
    gh run list --repo $REPO --branch $BRANCH --limit 5 --json status,conclusion,createdAt,displayTitle,url | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
for run in data:
    status = run['status']
    conclusion = run.get('conclusion', 'running')
    title = run['displayTitle'][:60]
    created = run['createdAt'][:19].replace('T', ' ')
    url = run['url']
    
    # Status emoji
    if status == 'completed':
        if conclusion == 'success':
            emoji = '✅'
        elif conclusion == 'failure':
            emoji = '❌'
        else:
            emoji = '⚠️'
    else:
        emoji = '🔄'
    
    print(f'{emoji} {status}/{conclusion} - {title}')
    print(f'   🕐 {created} - {url}')
    print()
"
    
    echo "🔗 Monitor live at: https://github.com/$REPO/actions"
    
else
    echo "⚠️  GitHub CLI not available"
    echo "🔗 Check pipeline manually at: https://github.com/$REPO/actions"
fi

echo
echo "🎯 Expected Pipeline Stages:"
echo "============================"
echo "1. 🔍 Quality & Security - Code quality, linting, security scans"
echo "2. 📊 Code Review - Complexity analysis, quality scoring" 
echo "3. 🧪 Test Suite - 88% coverage target, multi-version testing"
echo "4. 🔍 Search Tests - Search functionality validation"
echo "5. 🌱 Eco & Accessibility - Environmental impact, accessibility audit"
echo "6. 🚀 Deploy - Automatic deployment to Render"
echo "7. ✅ Verify - Post-deployment verification"

echo
echo "📈 Success Indicators:"
echo "====================="
echo "✅ All stages pass with green checkmarks"
echo "✅ Test coverage ≥ 88%"
echo "✅ Eco score ≥ 70"
echo "✅ Accessibility score ≥ 80"
echo "✅ Render deployment succeeds"
echo "✅ Version 2.1.1 badge appears on live site"

echo
echo "🔍 Live Monitoring:"
echo "=================="
echo "• GitHub Actions: https://github.com/$REPO/actions"
echo "• Live App: https://moodtunes-pwa.onrender.com/"
echo "• Version Check: Run ./scripts/check_deployment.sh after pipeline completes"

echo