# path: src/recognition/call_pattern_store.py

"""
CallPatternStore

Extended with topological summary capabilities for vision and call patterns.

Supports storing and querying recognition patterns from:
- Digital calls (voice verification)
- Vision detections (Instagram story zoom tags, etc.)

Includes basic topological metadata for future TDA/persistence landscape analysis.
"""

from typing import Any, Dict, List, Optional
import time


class CallPatternStore:
    def __init__(self, node_id: str = "default"):
        self.node_id = node_id
        self.stored_patterns: List[Dict[str, Any]] = []
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.vision_patterns: List[Dict[str, Any]] = []

    def store_call_event(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event["stored_at"] = time.time()
        self.stored_patterns.append(event)

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

    def store_vision_pattern(self, pattern: Dict[str, Any]) -> None:
        """Store vision detection patterns (e.g. from VisionTextEngine)."""
        pattern = dict(pattern)
        pattern["stored_at"] = time.time()
        self.vision_patterns.append(pattern)

        # Also store as general pattern for unified querying
        self.stored_patterns.append({
            "type": "vision_pattern",
            **pattern
        })

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_profiles.get(user_id)

    def query_recognition_patterns(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = self.stored_patterns[-limit:]
        if filters:
            results = [p for p in results if all(p.get(k) == v for k, v in filters.items())]
        return results

    def get_topological_summary(self) -> Dict[str, Any]:
        """
        Returns summary with basic topological metadata.
        Future versions will include full TDA persistence landscapes.
        """
        total_patterns = len(self.stored_patterns)
        vision_count = len(self.vision_patterns)
        call_count = total_patterns - vision_count

        human_rate = self._calculate_human_rate()

        return {
            "total_patterns": total_patterns,
            "vision_patterns": vision_count,
            "call_patterns": call_count,
            "unique_users": len(self.user_profiles),
            "human_verification_rate": human_rate,
            "topological_density_estimate": min(1.0, total_patterns / 100.0)  # placeholder
        }

    def _calculate_human_rate(self) -> float:
        if not self.stored_patterns:
            return 0.0
        verified = sum(1 for p in self.stored_patterns if p.get("is_human_verified"))
        return verified / len(self.stored_patterns)
