#!/bin/bash
# Helper script to check and apply Black formatting before committing

echo "🖤 Checking code formatting with Black..."

# Check if Black would make changes
if black --check --diff . > /dev/null 2>&1; then
    echo "✅ Code is already properly formatted!"
else
    echo "⚠️  Code needs formatting. Applying Black formatting..."
    black .
    echo "✅ Black formatting applied successfully!"
    
    # Show what was changed
    echo ""
    echo "📝 Files that were reformatted:"
    git diff --name-only
fi

echo ""
echo "🧪 Running quick test to ensure everything still works..."
python -m pytest --tb=line -q

if [ $? -eq 0 ]; then
    echo "✅ Tests pass! Ready to commit."
else
    echo "❌ Tests failed! Please fix issues before committing."
    exit 1
fi