# CI/CD Pipeline Reuse Guide

## 🔄 Framework-Specific Adaptations

### Python Applications
```yaml
# Detection Step
- name: Validate Python project
  run: |
    if [ ! -f "requirements.txt" ]; then
      echo "❌ requirements.txt not found"
      exit 1
    fi

# Dependencies
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

# Tests
- name: Run tests with coverage
  run: |
    python -m pytest -v --cov=. --cov-report=term-missing --cov-config=.coveragerc
```

### Node.js Applications
```yaml
# Detection Step
- name: Validate Node.js project
  run: |
    if [ ! -f "package.json" ]; then
      echo "❌ package.json not found"
      exit 1
    fi

# Dependencies
- name: Install dependencies
  run: |
    npm ci

# Tests
- name: Run tests with coverage
  run: |
    npm run test:coverage
```

### Go Applications
```yaml
# Detection Step
- name: Validate Go project
  run: |
    if [ ! -f "go.mod" ]; then
      echo "❌ go.mod not found"
      exit 1
    fi

# Dependencies
- name: Download dependencies
  run: |
    go mod download

# Tests
- name: Run tests with coverage
  run: |
    go test -v -race -coverprofile=coverage.out ./...
```

## 🛠️ Universal Components (No Changes Needed)

### 1. Quality Gates Structure
- Sequential job dependencies
- Artifact collection
- Conditional deployment
- Multi-environment testing

### 2. Security Scanning Pattern
- Branch-based triggering
- Parallel execution
- Report generation
- Quality thresholds

### 3. Documentation Scoring
- README analysis
- Code documentation detection
- Professional scoring metrics

## 📋 Customization Checklist

### Required Changes:
- [ ] Update application detection logic
- [ ] Modify dependency installation
- [ ] Adapt test execution commands
- [ ] Update deployment targets
- [ ] Customize eco_check.py for your bundle analysis

### Optional Enhancements:
- [ ] Add framework-specific linting
- [ ] Include additional security tools
- [ ] Customize quality thresholds
- [ ] Add performance benchmarks
- [ ] Include database migrations

## 🎯 Quality Standards (Reusable)

### Thresholds:
- Excellent: ≥80/100
- Good: ≥70/100
- Acceptable: ≥60/100

### Coverage Targets:
- Production Code: ≥80%
- Critical Functions: ≥90%
- Overall Project: ≥75%

### Complexity Limits:
- Average Complexity: ≤7
- Max Function Complexity: ≤15
- Eco Score Target: ≥70

This pipeline architecture is designed for maximum reusability across different technology stacks!

## 📱 UI Optimizations Included

### 1080x2040 Resolution Optimization
The application includes specialized CSS optimizations for ultra-tall mobile displays (1080x2040 and similar):

- **Smart Layout Adaptation**: Sections dynamically hide/show when playlist is active
- **No-Scroll Experience**: All content fits within viewport when playlist is displayed  
- **Compact UI Elements**: Reduced padding and spacing for maximum content visibility
- **Dynamic Class Management**: JavaScript adds `playlist-active` class to trigger optimizations

This ensures users on modern mobile devices never need to scroll to see their playlist!