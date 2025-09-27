// MoodTunes JavaScript functionality

// Configuration constants
const LOADING_TIMEOUT = 10000; // 10 seconds
const ERROR_TIMEOUT = 2000; // 2 seconds

// DOM Elements
const moodSelect = document.getElementById('mood');
const loadingDiv = document.getElementById('loading');
const spotifyPlayer = document.getElementById('spotify-player');
const spotifyIframe = document.getElementById('spotify-iframe');

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (moodSelect) {
        moodSelect.addEventListener('change', handleMoodChange);
    }
    
    // Add event listener for close button (removing inline onclick)
    const closeButton = document.getElementById('close-player-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closePlayer);
        
        // Add keyboard support for close button
        closeButton.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                closePlayer();
            }
        });
    }
    
    // Add event listeners for quick mood buttons
    const quickMoodButtons = document.querySelectorAll('.mood-quick-btn');
    quickMoodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const mood = this.getAttribute('data-mood');
            const moodText = this.textContent.trim();
            
            // Update the select element
            if (moodSelect) {
                moodSelect.value = mood;
            }
            
            // Trigger the mood selection
            showLoadingState(moodText);
            fetchPlaylist(mood, moodText);
            
            // Announce to screen readers
            announceToScreenReader(`Selected ${moodText} mood from quick selection`);
        });
    });
});

// Handle mood selection change
function handleMoodChange() {
    if (this.value) {
        const selectedMood = this.value;
        const moodText = this.options[this.selectedIndex].text;
        
        showLoadingState(moodText);
        fetchPlaylist(selectedMood, moodText);
    }
}

// Show loading state with selected mood
function showLoadingState(moodText) {
    loadingDiv.innerHTML = `<span role="img" aria-label="musical note">🎵</span> Opening ${moodText} playlist...`;
    loadingDiv.style.display = 'block';
    loadingDiv.setAttribute('aria-busy', 'true');
}

// Fetch playlist from server
function fetchPlaylist(selectedMood, moodText) {
    fetch('/get-playlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'mood=' + encodeURIComponent(selectedMood)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.playlist && data.embed_url) {
            showPlaylist(data.embed_url, moodText);
        } else {
            throw new Error('Invalid response format');
        }
    })
    .catch(error => {
        console.error('Error fetching playlist:', error);
        showErrorState(error.message);
    });
}

// Show successful playlist load
function showPlaylist(embedUrl, moodText) {
    // Load embedded player
    spotifyIframe.src = embedUrl;
    
    // Update fallback link for accessibility
    const fallbackLink = document.getElementById('spotify-fallback-link');
    if (fallbackLink) {
        fallbackLink.href = embedUrl.replace('/embed/', '/');
    }
    
    spotifyPlayer.style.display = 'block';
    
    // Show success message with proper ARIA
    loadingDiv.innerHTML = `<span role="img" aria-label="checkmark">✅</span> ${moodText} playlist loaded!`;
    loadingDiv.style.display = 'block';
    loadingDiv.setAttribute('aria-busy', 'false');
    
    // Announce to screen readers
    announceToScreenReader(`${moodText} playlist has been loaded and is now playing`);
    
    // Focus management - move focus to the player region
    setTimeout(() => {
        const playerHeading = document.getElementById('player-heading');
        if (playerHeading) {
            playerHeading.focus();
        }
    }, 500);
    
    // Reset after timeout
    setTimeout(() => {
        resetUI();
    }, LOADING_TIMEOUT);
}

// Show error state
function showErrorState(errorMessage) {
    loadingDiv.innerHTML = `<span role="img" aria-label="error">❌</span> Error: ${errorMessage}`;
    loadingDiv.style.display = 'block';
    loadingDiv.setAttribute('aria-busy', 'false');
    
    // Announce error to screen readers
    announceToScreenReader(`Error occurred: ${errorMessage}`);
    
    setTimeout(() => {
        resetUI();
    }, ERROR_TIMEOUT);
}

// Reset UI to initial state
function resetUI() {
    loadingDiv.style.display = 'none';
    loadingDiv.innerHTML = '<span role="img" aria-label="musical note">🎵</span> Opening your playlist...';
    loadingDiv.removeAttribute('aria-busy');
    if (moodSelect) {
        moodSelect.value = '';
        // Return focus to the select element
        moodSelect.focus();
    }
}

// Function to close the embedded player
function closePlayer() {
    spotifyPlayer.style.display = 'none';
    spotifyIframe.src = '';
    
    // Announce closure to screen readers
    announceToScreenReader('Music player closed');
    
    // Return focus to mood selector
    if (moodSelect) {
        moodSelect.focus();
    }
}

// Helper function to announce messages to screen readers
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'assertive');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'visually-hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Make closePlayer globally available (though it's now primarily handled by event listeners)
window.closePlayer = closePlayer;