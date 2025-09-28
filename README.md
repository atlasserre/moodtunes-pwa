# 🎵 MoodTunes PWA

> **Your Personal Music Mood Companion** -## 📚 Documentation

📖 **[Complete Documentation](docs/README.md)** - Comprehensive guide covering:
- Development setup and project structure
- Deployment instructions and security
- Testing and CI/CD pipeline  
- Search functionality and customization
- PWA features and mobile setup
- Troubleshooting and monitoring

🔍 **[Search Integration Guide](docs/SEARCH_CI_CD_INTEGRATION.md)** - Technical details on search functionality and automated testing

🛡️ **[Quality Gates Guide](docs/QUALITY_GATES_GUIDE.md)** - Complete quality assurance system covering:
- Code quality thresholds and scoring
- Environmental impact assessment (Eco Score)
- Accessibility compliance checking
- Security and performance gates
- Local development quality tools

## 🔧 Development Workflow

Before committing code changes, always run the formatting and quality checker:

```bash
./check_and_format.sh
```

This script will:
- ✅ Check and apply Black code formatting
- 🧪 Run quick tests to ensure functionality
- 📝 Show what files were reformatted
- 🚫 Prevent commits if tests fail

**Why this matters:** Our CI/CD pipeline has strict quality gates including Black formatting checks. Running this script locally prevents pipeline failures and maintains code quality.

📊 **[Quality Gates Summary](docs/QUALITY_GATES_SUMMARY.md)** - Implementation status and next stepsive Web App that curates Spotify playlists based on your current mood.

![MoodTunes Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![PWA](https://img.shields.io/badge/PWA-Ready-purple)

## ✨ Features

🎵 **15 Curated Mood Playlists** - From happy hits to deep focus music  
🔍 **Smart Search** - Find playlists with keywords like "workout", "chill", "focus"  
📱 **Progressive Web App** - Install on your phone like a native app  
⏰ **Time-Based Suggestions** - Smart recommendations based on time of day  
🎯 **Recent History** - Quick access to recently played moods  
🌐 **Offline Ready** - Core functionality works without internet  

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/atlasserre/moodtunes-pwa.git
cd moodtunes-pwa

# Install and run
pip install -r requirements.txt
python app.py

# Visit: http://localhost:5000
```

## 🎯 Mood Categories

- **😊 Emotional** - Happy, Sad, Romantic, Angry, Uplifting, Nostalgic, Melancholy
- **⚡ Energy & Activity** - Energetic, Motivated, Party, Running, Chill  
- **🧠 Mental State** - Focused, Meditative, Sleepy

## 🔍 Smart Search

Try searching for:
- **Single Results**: "happy", "study", "workout", "meditation"  
- **Multiple Options**: "positive", "calm", "peaceful", "inspiring"

## 📱 PWA Installation

1. Visit the app on mobile
2. Tap "Add to Home Screen" 
3. Install and enjoy native app experience!

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v --cov=app
```

## 🚀 Deployment

**Render.com** (One-click deploy):
- Build: `pip install -r requirements.txt`
- Start: `python app.py`
- Set `SECRET_KEY` environment variable

## � Documentation

📖 **[Complete Documentation](docs/README.md)** - Comprehensive guide covering:
- Development setup and project structure
- Deployment instructions and security
- Testing and CI/CD pipeline  
- Search functionality and customization
- PWA features and mobile setup
- Troubleshooting and monitoring

🔍 **[Search Integration Guide](docs/SEARCH_CI_CD_INTEGRATION.md)** - Technical details on search functionality and automated testing

## � Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript  
- **PWA**: Service Worker, Web App Manifest
- **Testing**: pytest with comprehensive coverage
- **CI/CD**: GitHub Actions with automated quality checks
- **Deployment**: Render.com ready

## 📊 Quality Assurance

✅ **5-Tier Quality Gates** - Code quality, eco score, accessibility, testing, performance  
✅ **Environmental Impact** - CO2 tracking and energy optimization (1.8g CO2 per 1K visits)  
✅ **Accessibility Compliance** - WCAG 2.1 AA standards with automated testing  
✅ **Security Hardening** - Vulnerability scanning and secure coding practices  
✅ **Production Ready** - Comprehensive quality gates prevent bad deployments  

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Add tests for new functionality
4. Ensure all tests pass (`python -m pytest tests/`)
5. Submit pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for music lovers everywhere** 🎵

*Turn your mood into music, instantly.*