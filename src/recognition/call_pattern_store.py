# path: src/recognition/call_pattern_store.py

"""
CallPatternStore

Integration point in JuniorMemSys-Suite for storing and querying
recognition patterns derived from digital/mobile calling data.

This allows long-term topological memory of:
- Voice verification outcomes (human vs bot patterns over time)
- User-specific voice profiles from repeated calls
- Temporal patterns in call behavior
- Topological features (TDA persistence) of voice feature sequences

Designed to be called from JuniorHome's DigitalCallManager
via the MemoryBackend abstraction.
"""

from typing import Any, Dict, List, Optional
import time


class CallPatternStore:
    def __init__(self, node_id: str = "default"):
        self.node_id = node_id
        self.stored_patterns: List[Dict[str, Any]] = []
        self.user_profiles: Dict[str, Dict[str, Any]] = {}

    def store_call_event(self, event: Dict[str, Any]) -> None:
        """
        Store a structured call event from DigitalCallManager.

        Expected event keys:
        - call_id
        - type (call_accepted, call_unmuted, call_ended, etc.)
        - timestamp
        - verification_score or features (from quant/theoretical engine)
        - is_human_verified
        - duration (for ended calls)
        """
        event = dict(event)  # copy
        event["stored_at"] = time.time()
        self.stored_patterns.append(event)

        # Update user profile if user_id or profile info is present
        user_id = event.get("user_id") or event.get("call_id")
        if user_id:
            if user_id not in self.user_profiles:
                self.user_profiles[user_id] = {
                    "total_calls": 0,
                    "human_verified_count": 0,
                    "last_seen": None,
                    "voice_features_history": []
                }
            profile = self.user_profiles[user_id]
            profile["total_calls"] += 1
            profile["last_seen"] = event.get("timestamp")

            if event.get("is_human_verified"):
                profile["human_verified_count"] += 1

            if "audio_features" in event or "verification_score" in event:
                profile["voice_features_history"].append({
                    "timestamp": event.get("timestamp"),
                    "features": event.get("audio_features"),
                    "score": event.get("verification_score")
                })

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_profiles.get(user_id)

    def query_recognition_patterns(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Query stored patterns.
        In full implementation this would use TDA / topological queries.
        """
        results = self.stored_patterns[-limit:]
        if filters:
            # Simple filtering for now; later replace with topological queries
            results = [p for p in results if all(p.get(k) == v for k, v in filters.items())]
        return results

    def get_topological_summary(self) -> Dict[str, Any]:
        """
        Placeholder for future TDA-based summary of voice pattern topology.
        """
        return {
            "total_patterns_stored": len(self.stored_patterns),
            "unique_users": len(self.user_profiles),
            "human_verification_rate": self._calculate_human_rate()
        }

    def _calculate_human_rate(self) -> float:
        if not self.stored_patterns:
            return 0.0
        verified = sum(1 for p in self.stored_patterns if p.get("is_human_verified"))
        return verified / len(self.stored_patterns)
