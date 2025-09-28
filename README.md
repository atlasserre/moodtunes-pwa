# MoodTunes 🎵

A simple Flask web application that matches your current mood to curated Spotify playlists.

## Features

- **Mood Selection**: Choose from 15 different moods covering various emotional states and activities
- **Smart Suggestions**: Time-based mood recommendations that adapt to your daily routine
- **Recent Moods**: Quick access to your last 3 selected moods for easy replay
- **Organized Categories**: Moods grouped by Emotional, Energy & Activity, and Mental State
- **Spotify Integration**: Embedded Spotify player for immediate playlist access
- **Responsive Design**: Clean, user-friendly interface with full accessibility support
- **Real-time Loading**: Visual feedback during playlist loading

## Setup

### Prerequisites
- Python 3.7 or higher
- Internet connection for Spotify embeds

### Installation

1. Clone or download the project to your local machine
2. Navigate to the project directory:
   ```bash
   cd MoodTunes
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Using the batch file (Windows)
Double-click `start_moodtunes.bat` or run it from command line.

#### Option 2: Direct Python execution
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. Open your web browser and go to `http://localhost:5000`
2. **Quick Selection**: Click on time-based suggestions or recent moods for instant access
3. **Browse Categories**: Use the organized dropdown menu to explore all 15 moods
4. Wait for the playlist to load in the embedded player
5. Enjoy your personalized music experience!
6. Use the "Close Player" button to hide the player when done

### Smart Features

**🕐 Time-Based Suggestions**: The app automatically suggests moods based on the current time:
- **Morning (6-9 AM)**: Uplifting, Motivated, Energetic
- **Late Morning (9AM-12PM)**: Focused, Motivated, Happy
- **Lunch (12-2 PM)**: Chill, Happy, Uplifting
- **Afternoon (2-5 PM)**: Focused, Energetic, Motivated
- **Evening (5-8 PM)**: Chill, Happy, Party
- **Night (8-10 PM)**: Romantic, Chill, Nostalgic
- **Late Night (10PM-6AM)**: Sleepy, Meditative, Chill

**🔄 Recent Moods**: Your last 3 mood selections are saved and displayed for quick access

## Project Structure

```
MoodTunes/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── start_moodtunes.bat # Windows batch file for easy startup
├── static/
│   ├── style.css      # Application styles
│   └── script.js      # JavaScript functionality
└── templates/
    └── index.html     # Main HTML template
```

## Playlist Sources

All playlists are curated Spotify playlists:

### **Original Moods**
- **😊 Happy**: Happy Hits
- **😢 Sad**: Sad Songs  
- **💪 Energetic**: Beast Mode
- **😌 Chill**: Lofi Chill
- **❤️ Romantic**: Love Pop

### **New Mood Additions**
- **🔥 Motivated**: Beast Mode (Workout)
- **😴 Sleepy**: Sleep
- **🤔 Focused**: Deep Focus
- **🎉 Party**: Pop Rising
- **😌 Nostalgic**: All Out 2010s
- **😠 Angry**: Heavy Metal
- **🌧️ Melancholy**: Atmospheric Calm
- **☀️ Uplifting**: Good Vibes
- **🧘 Meditative**: Peaceful Piano
- **🏃 Running**: Power Workout

## Technical Notes

- Built with Flask framework
- Progressive Web App (PWA) with offline support
- Uses Spotify's embedded player (no API key required)
- Includes error handling and input validation
- Logging enabled for debugging purposes
- Full accessibility compliance (WCAG 2.1 AA)
- Mobile-optimized with service worker caching

## 📱 Mobile App Installation

**Your MoodTunes app can be installed on Android phones like a native app!**

### Quick Setup:
1. **Start the app**: `python app.py`
2. **Find your IP**: `ipconfig | findstr IPv4`
3. **On Android**: Open `http://YOUR_IP:5000` in Chrome
4. **Install**: Tap the install prompt or "Add to Home screen"

📋 **Detailed instructions**: See `MOBILE_SETUP.md`

### PWA Features:
- 🏠 **Home screen icon** - Launch like any app
- 📱 **Standalone mode** - No browser interface
- 🔄 **Offline support** - Works without internet
- ⚡ **App shortcuts** - Quick access to favorite moods
- 🎯 **Touch optimized** - Perfect mobile experience

## Troubleshooting

- **Playlist won't load**: Check your internet connection
- **Server won't start**: Ensure Flask is installed (`pip install flask`)
- **Port already in use**: Flask will automatically find an available port
- **PWA won't install**: Ensure icons exist in `/static/icons/` folder
- **Can't access from phone**: Check same WiFi network and firewall settings

---

*Created as a personal mood-music matching tool with mobile PWA support* 🎼📱