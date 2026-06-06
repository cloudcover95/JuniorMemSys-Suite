# path: src/recognition/call_pattern_store.py

"""
CallPatternStore

Deeper topological memory support for vision and call recognition patterns.

Features:
- Persistent storage of vision tag detections with topological metadata
- Basic persistence landscape simulation (for future full TDA)
- Security-conscious storage (integrity hashes for patterns)
- Querying by topological similarity (placeholder for real TDA)

Integrates with VisionTextEngine and DigitalCallManager.
"""

from typing import Any, Dict, List, Optional
import time
import hashlib


class CallPatternStore:
    def __init__(self, node_id: str = "default"):
        self.node_id = node_id
        self.stored_patterns: List[Dict[str, Any]] = []
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.vision_patterns: List[Dict[str, Any]] = []
        self.topological_index: Dict[str, List[str]] = {}  # Simple index for similarity

    def _compute_integrity_hash(self, data: Dict[str, Any]) -> str:
        """Security: Compute integrity hash for stored patterns."""
        serialized = str(sorted(data.items())).encode()
        return hashlib.sha256(serialized).hexdigest()

    def store_call_event(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event["stored_at"] = time.time()
        event["integrity_hash"] = self._compute_integrity_hash(event)
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

    def store_vision_pattern(self, pattern: Dict[str, Any]) -> None:
        pattern = dict(pattern)
        pattern["stored_at"] = time.time()
        pattern["integrity_hash"] = self._compute_integrity_hash(pattern)
        pattern["topological_signature"] = self._generate_topological_signature(pattern)

        self.vision_patterns.append(pattern)
        self.stored_patterns.append({
            "type": "vision_pattern",
            **pattern
        })

        # Update simple topological index
        sig = pattern["topological_signature"]
        if sig not in self.topological_index:
            self.topological_index[sig] = []
        self.topological_index[sig].append(pattern.get("detected_tags", ["unknown"])[0] if pattern.get("detected_tags") else "unknown")

    def _generate_topological_signature(self, pattern: Dict[str, Any]) -> str:
        """Basic topological signature (placeholder for real TDA persistence)."""
        tags = pattern.get("detected_tags", [])
        zoom = pattern.get("zoom_level", 1.0)
        # Simple signature based on tag count and zoom level
        return f"t{len(tags)}_z{int(zoom)}"

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_profiles.get(user_id)

    def query_recognition_patterns(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = self.stored_patterns[-limit:]
        if filters:
            results = [p for p in results if all(p.get(k) == v for k, v in filters.items())]
        return results

    def query_by_topological_similarity(self, signature: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query patterns with similar topological signatures."""
        similar = []
        for sig, items in self.topological_index.items():
            if sig == signature or self._signature_similarity(sig, signature) > 0.7:
                similar.extend(items)
        return similar[:limit]

    def _signature_similarity(self, sig1: str, sig2: str) -> float:
        """Simple similarity between topological signatures."""
        # Placeholder - in real TDA this would use persistence diagram distance
        common = len(set(sig1) & set(sig2))
        total = len(set(sig1) | set(sig2))
        return common / total if total > 0 else 0.0

    def get_topological_summary(self) -> Dict[str, Any]:
        total = len(self.stored_patterns)
        vision = len(self.vision_patterns)
        return {
            "total_patterns": total,
            "vision_patterns": vision,
            "call_patterns": total - vision,
            "unique_users": len(self.user_profiles),
            "human_verification_rate": self._calculate_human_rate(),
            "topological_clusters": len(self.topological_index),
            "average_cluster_size": sum(len(v) for v in self.topological_index.values()) / max(len(self.topological_index), 1)
        }

    def _calculate_human_rate(self) -> float:
        if not self.stored_patterns:
            return 0.0
        verified = sum(1 for p in self.stored_patterns if p.get("is_human_verified"))
        return verified / len(self.stored_patterns)
