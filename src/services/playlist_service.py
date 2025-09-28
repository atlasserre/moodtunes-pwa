"""
Service layer for playlist business logic.

Implements core business rules and orchestrates data flow between repositories and controllers.
This layer contains the application's business logic and use cases.
"""

from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
import asyncio

from ..models.playlist import (
    UserPlaylist, 
    CuratedMoodPlaylist, 
    SearchResult, 
    PlaylistType,
    UserSession
)
from ..repositories.playlist_repository import PlaylistRepositoryInterface


class PlaylistService:
    """
    Core business logic for playlist management.
    
    Handles:
    - Unified search across user and curated playlists
    - Smart recommendations and suggestions
    - Usage tracking and analytics
    - Playlist ranking and scoring
    """
    
    def __init__(self, repository: PlaylistRepositoryInterface):
        self.repository = repository
        self._recommendation_cache: Dict[str, Any] = {}
    
    def search_playlists(
        self, 
        query: str, 
        max_results: int = 20
    ):
        """
        Search user playlists using the database repository.
        
        Returns list of matching playlists.
        """
        # Search user playlists using the repository
        return self.repository.search_playlists(query, max_results)
                    "popularity_score": playlist.popularity_score
                }
            )
            results.append(result)
        
        # Search curated mood playlists if requested
        if include_curated:
            curated_results = await self._search_curated_playlists(query, user_session)
            results.extend(curated_results[:max_results//2])
        
        # Sort by match score, then by type preference (user playlists first)
        results.sort(key=lambda r: (r.match_score, r.type == PlaylistType.USER_PLAYLIST), reverse=True)
        
        return results[:max_results]
    
    async def get_smart_recommendations(self, user_session: UserSession) -> Dict[str, List[SearchResult]]:
        """
        Generate smart playlist recommendations based on user behavior.
        
        Returns categorized recommendations:
        - Recently played
        - Based on favorites
        - Time-based suggestions
        - Similar to recent activity
        """
        cache_key = f"recommendations_{user_session.session_id}"
        
        # Check cache (in real app, this would have TTL)
        if cache_key in self._recommendation_cache:
            return self._recommendation_cache[cache_key]
        
        user_playlists = await self.repository.get_user_playlists(user_session)
        
        recommendations = {
            "recently_played": self._get_recently_played_recommendations(user_playlists, user_session),
            "favorites": self._get_favorite_recommendations(user_playlists, user_session),
            "time_based": await self._get_time_based_recommendations(user_session),
            "similar_to_recent": await self._get_similar_recommendations(user_playlists, user_session)
        }
        
        # Cache recommendations
        self._recommendation_cache[cache_key] = recommendations
        
        return recommendations
    
    async def track_playlist_play(self, playlist_id: str, user_session: UserSession) -> None:
        """Track playlist play for analytics and recommendations"""
        await self.repository.update_playlist_usage(playlist_id, user_session)
        
        # Clear recommendation cache to force refresh
        cache_key = f"recommendations_{user_session.session_id}"
        if cache_key in self._recommendation_cache:
            del self._recommendation_cache[cache_key]
    
    async def get_playlist_analytics(self, user_session: UserSession) -> Dict[str, Any]:
        """Get user playlist analytics and insights"""
        user_playlists = await self.repository.get_user_playlists(user_session)
        
        total_playlists = len(user_playlists)
        total_tracks = sum(p.metadata.track_count for p in user_playlists)
        total_duration_hours = sum(p.metadata.duration_ms for p in user_playlists) / (1000 * 3600)
        
        recently_played = [p for p in user_playlists if p.is_recently_played]
        favorites = [p for p in user_playlists if p.is_favorite]
        
        # Most played playlists
        most_played = sorted(user_playlists, key=lambda p: p.play_count, reverse=True)[:5]
        
        # Extract common tags
        all_tags = []
        for playlist in user_playlists:
            all_tags.extend(playlist.tags)
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_playlists": total_playlists,
            "total_tracks": total_tracks,
            "total_duration_hours": round(total_duration_hours, 1),
            "recently_played_count": len(recently_played),
            "favorites_count": len(favorites),
            "most_played": [
                {
                    "name": p.metadata.name,
                    "play_count": p.play_count,
                    "last_played": p.last_played
                } for p in most_played
            ],
            "top_genres": [{"tag": tag, "count": count} for tag, count in top_tags],
            "average_playlist_length": round(total_tracks / total_playlists if total_playlists > 0 else 0, 1)
        }
    
    def _calculate_user_playlist_relevance(
        self, 
        playlist: UserPlaylist, 
        query: str, 
        user_session: UserSession
    ) -> float:
        """Calculate relevance score for user playlist based on query and user preferences"""
        base_score = 0.0
        query_lower = query.lower().strip()
        
        # Text matching scores
        if query_lower == playlist.metadata.name.lower():
            base_score = 1.0
        elif query_lower in playlist.metadata.name.lower():
            base_score = 0.8
        elif playlist.metadata.description and query_lower in playlist.metadata.description.lower():
            base_score = 0.6
        elif any(query_lower in tag.lower() for tag in playlist.tags):
            base_score = 0.7
        
        # Boost score based on user preferences
        if playlist.is_favorite:
            base_score += 0.1
        
        if playlist.is_recently_played:
            base_score += 0.05
        
        # Boost based on play count (normalized)
        play_count_boost = min(0.1, playlist.play_count * 0.002)
        base_score += play_count_boost
        
        return min(1.0, base_score)
    
    async def _search_curated_playlists(self, query: str, user_session: UserSession) -> List[SearchResult]:
        """Search curated mood playlists"""
        # This would integrate with your existing mood playlist data
        # For now, return empty list - we'll integrate this later
        return []
    
    def _get_recently_played_recommendations(
        self, 
        playlists: List[UserPlaylist], 
        user_session: UserSession
    ) -> List[SearchResult]:
        """Get recommendations based on recently played playlists"""
        recent_playlists = [p for p in playlists if p.is_recently_played]
        recent_playlists.sort(key=lambda p: p.last_played or datetime.min, reverse=True)
        
        results = []
        for playlist in recent_playlists[:5]:
            result = SearchResult(
                playlist_id=playlist.metadata.id,
                name=playlist.metadata.name,
                type=PlaylistType.USER_PLAYLIST,
                match_score=0.9,  # High score for recent activity
                metadata={
                    "description": playlist.metadata.description,
                    "last_played": playlist.last_played,
                    "reason": "Recently played"
                }
            )
            results.append(result)
        
        return results
    
    def _get_favorite_recommendations(
        self, 
        playlists: List[UserPlaylist], 
        user_session: UserSession
    ) -> List[SearchResult]:
        """Get recommendations based on favorite playlists"""
        favorites = [p for p in playlists if p.is_favorite]
        favorites.sort(key=lambda p: p.popularity_score, reverse=True)
        
        results = []
        for playlist in favorites[:5]:
            result = SearchResult(
                playlist_id=playlist.metadata.id,
                name=playlist.metadata.name,
                type=PlaylistType.USER_PLAYLIST,
                match_score=0.85,
                metadata={
                    "description": playlist.metadata.description,
                    "is_favorite": True,
                    "reason": "One of your favorites"
                }
            )
            results.append(result)
        
        return results
    
    async def _get_time_based_recommendations(self, user_session: UserSession) -> List[SearchResult]:
        """Get recommendations based on current time of day"""
        # This would integrate with your existing time-based mood suggestions
        # For now, return empty list - we'll integrate this later
        return []
    
    async def _get_similar_recommendations(
        self, 
        playlists: List[UserPlaylist], 
        user_session: UserSession
    ) -> List[SearchResult]:
        """Get recommendations similar to recently played playlists"""
        recent_playlist_ids = user_session.recent_playlists[:3]
        recent_playlists = [p for p in playlists if p.metadata.id in recent_playlist_ids]
        
        if not recent_playlists:
            return []
        
        # Extract tags from recent playlists
        recent_tags = set()
        for playlist in recent_playlists:
            recent_tags.update(playlist.tags)
        
        # Find playlists with similar tags
        similar_playlists = []
        for playlist in playlists:
            if playlist.metadata.id not in recent_playlist_ids:  # Exclude already recent
                common_tags = set(playlist.tags) & recent_tags
                if common_tags:
                    similarity_score = len(common_tags) / len(recent_tags) if recent_tags else 0
                    similar_playlists.append((playlist, similarity_score))
        
        # Sort by similarity and popularity
        similar_playlists.sort(key=lambda x: (x[1], x[0].popularity_score), reverse=True)
        
        results = []
        for playlist, similarity in similar_playlists[:5]:
            result = SearchResult(
                playlist_id=playlist.metadata.id,
                name=playlist.metadata.name,
                type=PlaylistType.USER_PLAYLIST,
                match_score=0.7 + (similarity * 0.2),  # Base score + similarity bonus
                metadata={
                    "description": playlist.metadata.description,
                    "similarity_score": similarity,
                    "common_tags": list(set(playlist.tags) & recent_tags),
                    "reason": f"Similar to your recent listening"
                }
            )
            results.append(result)
        
        return results