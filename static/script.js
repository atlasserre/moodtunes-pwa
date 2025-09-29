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
    
    // Use event delegation for quick mood buttons (works even after DOM restoration)
    document.addEventListener('click', function(event) {
        // Check if clicked element is a quick mood button
        if (event.target.classList.contains('mood-quick-btn') || event.target.closest('.mood-quick-btn')) {
            const button = event.target.classList.contains('mood-quick-btn') ? event.target : event.target.closest('.mood-quick-btn');
            const mood = button.getAttribute('data-mood');
            const moodText = button.textContent.trim();
            
            // Update the select element
            if (moodSelect) {
                moodSelect.value = mood;
            }
            
            // Trigger the mood selection
            showLoadingState(moodText);
            fetchPlaylist(mood, moodText);
            
            // Announce to screen readers
            announceToScreenReader(`Selected ${moodText} mood from quick selection`);
        }
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
    // If there was a previous playlist, reset UI first to restore sections
    if (spotifyPlayer && spotifyPlayer.style.display === 'block') {
        console.log('Resetting UI for new mood selection');
        resetUI();
    }
    
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
    
    // Add class for optimization (hide other sections when playlist active)
    document.body.classList.add('playlist-active');
    console.log('Added playlist-active class:', document.body.classList.contains('playlist-active'));
    
    // Store and completely remove suggestions sections from DOM
    const suggestionsSection = document.querySelector('.suggestions-section');
    const recentSection = document.querySelector('.recent-section');
    
    // Store references and parent info for restoration
    window.removedSections = {
        suggestions: null,
        recent: null,
        suggestionsParent: null,
        recentParent: null,
        suggestionsNextSibling: null,
        recentNextSibling: null
    };
    
    if (suggestionsSection) {
        window.removedSections.suggestions = suggestionsSection.cloneNode(true);
        window.removedSections.suggestionsParent = suggestionsSection.parentNode;
        window.removedSections.suggestionsNextSibling = suggestionsSection.nextSibling;
        suggestionsSection.remove();
        console.log('Completely removed suggestions section from DOM');
    }
    if (recentSection) {
        window.removedSections.recent = recentSection.cloneNode(true);
        window.removedSections.recentParent = recentSection.parentNode;
        window.removedSections.recentNextSibling = recentSection.nextSibling;
        recentSection.remove();
        console.log('Completely removed recent section from DOM');
    }

    
    // Show permanent mood selection message to prevent layout shifts
    loadingDiv.innerHTML = `<span role="img" aria-label="selected">🎵</span> Selected: <strong>${moodText}</strong> playlist`;
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
    
    // NO AUTOMATIC RESET - keep loading message and layout stable
    // UI will only reset when user selects another mood or closes player
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
    
    // Remove class for optimization
    document.body.classList.remove('playlist-active');
    
    // Restore removed sections back to DOM
    if (window.removedSections) {
        if (window.removedSections.suggestions && window.removedSections.suggestionsParent) {
            if (window.removedSections.suggestionsNextSibling) {
                window.removedSections.suggestionsParent.insertBefore(
                    window.removedSections.suggestions, 
                    window.removedSections.suggestionsNextSibling
                );
            } else {
                window.removedSections.suggestionsParent.appendChild(window.removedSections.suggestions);
            }
            console.log('Restored suggestions section to DOM');
        }
        if (window.removedSections.recent && window.removedSections.recentParent) {
            if (window.removedSections.recentNextSibling) {
                window.removedSections.recentParent.insertBefore(
                    window.removedSections.recent, 
                    window.removedSections.recentNextSibling
                );
            } else {
                window.removedSections.recentParent.appendChild(window.removedSections.recent);
            }
            console.log('Restored recent section to DOM');
        }
        window.removedSections = null;
    }
    
    if (moodSelect) {
        moodSelect.value = '';
        // Return focus to the select element
        moodSelect.focus();
    }
}

// Function to close the embedded player
function closePlayer() {
    // Simple and reliable approach: refresh the page to get updated Recent section
    window.location.reload();
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

// =============================================================================
// SPOTIFY PLAYLIST SEARCH FUNCTIONALITY
// =============================================================================

// DOM Elements for search
const playlistSearchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-btn');
const searchResults = document.getElementById('search-results');
const searchResultsList = document.getElementById('search-results-list');
const searchLoading = document.getElementById('search-loading');

// Initialize search functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (playlistSearchInput && searchButton) {
        // Add event listeners
        searchButton.addEventListener('click', performPlaylistSearch);
        
        // Allow search on Enter key
        playlistSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performPlaylistSearch();
            }
        });
    }
});

// Perform playlist search
async function performPlaylistSearch() {
    const query = playlistSearchInput.value.trim();
    
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    
    if (query.length < 2) {
        alert('Please enter at least 2 characters');
        return;
    }
    
    // Show loading state
    searchButton.disabled = true;
    searchButton.innerHTML = '<span role="img" aria-label="searching">🔄</span> Searching...';
    searchLoading.style.display = 'block';
    searchResults.style.display = 'block';
    searchResultsList.innerHTML = '';
    
    try {
        // Call our Flask backend to search curated playlists
        const response = await fetch('/search-playlists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'query=' + encodeURIComponent(query)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.moods, query);
        } else {
            throw new Error(data.error || 'Search failed');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        searchResultsList.innerHTML = `
            <div class="error-message">
                <span role="img" aria-label="error">❌</span>
                Search failed: ${error.message}
                <br><small>Try a different search term or check your connection.</small>
            </div>
        `;
    } finally {
        // Reset button state
        searchButton.disabled = false;
        searchButton.innerHTML = '<span role="img" aria-label="search">🔍</span> Search';
        searchLoading.style.display = 'none';
    }
}

// Display search results
function displaySearchResults(moods, query) {
    if (!moods || moods.length === 0) {
        searchResultsList.innerHTML = `
            <div class="no-results">
                <span role="img" aria-label="no results">🎵</span>
                <h3>No moods found</h3>
                <p>Try keywords like "happy", "chill", "workout", "study", "focus", or "relax"</p>
            </div>
        `;
        return;
    }
    
    // If only one result, automatically select it
    if (moods.length === 1) {
        const mood = moods[0];
        searchResultsList.innerHTML = `
            <div class="single-result">
                <span role="img" aria-label="found">${mood.icon}</span>
                <p>Found perfect match: <strong>${mood.name}</strong></p>
                <p class="mood-description">${mood.description}</p>
            </div>
        `;
        
        // Automatically play the single result after a brief moment
        setTimeout(() => {
            selectMoodFromSearch(mood.mood_key, mood.name);
        }, 1000);
        
        announceToScreenReader(`Found perfect match: ${mood.name}. Loading playlist now.`);
        return;
    }
    
    // Multiple results - show selection list
    const moodCards = moods.map(mood => {
        return `
            <div class="mood-search-card" data-mood-key="${mood.mood_key}">
                <div class="mood-icon">${mood.icon}</div>
                <div class="mood-info">
                    <h3>${escapeHtml(mood.name)}</h3>
                    <div class="mood-description">${escapeHtml(mood.description)}</div>
                    <div class="mood-category">${escapeHtml(mood.category)}</div>
                </div>
                <div class="mood-actions">
                    <button class="select-mood-btn" onclick="selectMoodFromSearch('${mood.mood_key}', '${escapeHtml(mood.name)}')">
                        ${mood.icon} Select
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    searchResultsList.innerHTML = `
        <div class="multiple-results-header">
            <h3>Found ${moods.length} moods for "${escapeHtml(query)}"</h3>
            <p>Choose the mood that best fits what you're looking for:</p>
        </div>
        ${moodCards}
    `;
    
    // Announce results to screen readers
    announceToScreenReader(`Found ${moods.length} mood${moods.length === 1 ? '' : 's'} for "${query}". Please select one.`);
}

// Select mood from search results (integrates with existing mood selection system)
function selectMoodFromSearch(moodKey, moodName) {
    // Update the main mood selector if it exists
    if (moodSelect) {
        moodSelect.value = moodKey;
    }
    
    // Hide search results
    searchResults.style.display = 'none';
    
    // Clear search input
    playlistSearchInput.value = '';
    
    // Use existing mood selection logic
    showLoadingState(moodName);
    fetchPlaylist(moodKey, moodName);
    
    // Announce to screen readers
    announceToScreenReader(`Selected ${moodName} mood from search results`);
    
    // Scroll to player area
    setTimeout(() => {
        const player = document.getElementById('spotify-player');
        if (player) {
            player.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, 500);
}

// Utility function to format numbers (e.g., 1234 -> 1.2K)
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}