// PWA Installation and Offline Support
let deferredPrompt;
let isStandalone = false;

// Check if app is running in standalone mode
isStandalone = window.matchMedia('(display-mode: standalone)').matches || 
              window.navigator.standalone || 
              document.referrer.includes('android-app://');

// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Handle install prompt
window.addEventListener('beforeinstallprompt', (e) => {
  console.log('Install prompt triggered');
  
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  
  // Show install banner if not in standalone mode
  if (!isStandalone) {
    showInstallBanner();
  }
});

// Show install banner
function showInstallBanner() {
  const installBanner = document.getElementById('install-banner');
  const installBtn = document.getElementById('install-btn');
  const dismissBtn = document.getElementById('dismiss-install');
  
  if (installBanner && !localStorage.getItem('installDismissed')) {
    installBanner.style.display = 'block';
    
    // Install button click
    installBtn.addEventListener('click', () => {
      installBanner.style.display = 'none';
      
      if (deferredPrompt) {
        // Show the install prompt
        deferredPrompt.prompt();
        
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the install prompt');
            announceToScreenReader('MoodTunes has been installed');
          } else {
            console.log('User dismissed the install prompt');
          }
          deferredPrompt = null;
        });
      }
    });
    
    // Dismiss button click
    dismissBtn.addEventListener('click', () => {
      installBanner.style.display = 'none';
      localStorage.setItem('installDismissed', 'true');
    });
  }
}

// Handle app installation
window.addEventListener('appinstalled', (evt) => {
  console.log('App was installed');
  const installBanner = document.getElementById('install-banner');
  if (installBanner) {
    installBanner.style.display = 'none';
  }
  
  // Show success message
  announceToScreenReader('MoodTunes has been successfully installed as an app');
});

// Handle network status changes
window.addEventListener('online', () => {
  console.log('App is online');
  showNetworkStatus('You are back online!', 'success');
});

window.addEventListener('offline', () => {
  console.log('App is offline');
  showNetworkStatus('You are offline. Some features may be limited.', 'warning');
});

// Show network status messages
function showNetworkStatus(message, type) {
  const statusDiv = document.createElement('div');
  statusDiv.className = `network-status ${type}`;
  statusDiv.innerHTML = `
    <span role="img" aria-label="${type === 'success' ? 'connected' : 'disconnected'}">
      ${type === 'success' ? '🟢' : '🔴'}
    </span>
    ${message}
  `;
  
  document.body.appendChild(statusDiv);
  
  // Remove after 3 seconds
  setTimeout(() => {
    if (statusDiv.parentNode) {
      document.body.removeChild(statusDiv);
    }
  }, 3000);
  
  // Announce to screen readers
  announceToScreenReader(message);
}

// Handle URL shortcuts (from manifest shortcuts)
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const mood = urlParams.get('mood');
  
  if (mood && mood_playlists && mood_playlists[mood]) {
    // Auto-select mood if coming from shortcut
    const moodSelect = document.getElementById('mood');
    if (moodSelect) {
      moodSelect.value = mood;
      
      // Trigger mood selection
      const moodInfo = getMoodDisplayInfo(mood);
      if (moodInfo) {
        setTimeout(() => {
          showLoadingState(moodInfo.name);
          fetchPlaylist(mood, moodInfo.name);
        }, 500);
      }
    }
  }
});

// Helper function to get mood display info (if not available from main script)
function getMoodDisplayInfo(mood) {
  const moodData = {
    happy: { name: 'Happy', icon: '😊' },
    sad: { name: 'Sad', icon: '😢' },
    energetic: { name: 'Energetic', icon: '💪' },
    chill: { name: 'Chill', icon: '😌' },
    romantic: { name: 'Romantic', icon: '❤️' },
    motivated: { name: 'Motivated', icon: '🔥' },
    sleepy: { name: 'Sleepy', icon: '😴' },
    focused: { name: 'Focused', icon: '🤔' },
    party: { name: 'Party', icon: '🎉' },
    nostalgic: { name: 'Nostalgic', icon: '😌' },
    angry: { name: 'Angry', icon: '😠' },
    melancholy: { name: 'Melancholy', icon: '🌧️' },
    uplifting: { name: 'Uplifting', icon: '☀️' },
    meditative: { name: 'Meditative', icon: '🧘' },
    running: { name: 'Running', icon: '🏃' }
  };
  
  return moodData[mood] || null;
}

// Prevent zoom on double tap (better mobile experience)
let lastTouchEnd = 0;
document.addEventListener('touchend', function (event) {
  const now = (new Date()).getTime();
  if (now - lastTouchEnd <= 300) {
    event.preventDefault();
  }
  lastTouchEnd = now;
}, false);

// Handle device orientation changes
window.addEventListener('orientationchange', () => {
  // Small delay to ensure viewport has updated
  setTimeout(() => {
    // Force recalculation of viewport height for mobile browsers
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  }, 100);
});

// Set initial viewport height
const vh = window.innerHeight * 0.01;
document.documentElement.style.setProperty('--vh', `${vh}px`);