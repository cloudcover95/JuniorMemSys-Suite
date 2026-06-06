# path: src/recognition/call_pattern_store.py

"""
CallPatternStore

Added pattern prediction and rule-based inference over the graph.

This enables forward-looking reasoning (e.g. predicting future vision tags or call patterns based on current graph state).

Security and biological integration hooks included.
"""

from typing import Any, Dict, List, Optional, Set
import time
import hashlib


class CallPatternStore:
    def __init__(self, node_id: str = "default"):
        self.node_id = node_id
        self.stored_patterns: List[Dict[str, Any]] = []
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.vision_patterns: List[Dict[str, Any]] = []
        self.topological_index: Dict[str, List[str]] = {}
        self.pattern_graph: Dict[str, Set[str]] = {}
        self.event_signatures: Dict[str, str] = {}

    def _compute_integrity_hash(self, data: Dict[str, Any]) -> str:
        serialized = str(sorted(data.items())).encode()
        return hashlib.sha256(serialized).hexdigest()

    def _sign_event(self, event: Dict[str, Any]) -> str:
        return self._compute_integrity_hash(event)

    def store_call_event(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event["stored_at"] = time.time()
        event["integrity_hash"] = self._compute_integrity_hash(event)
        event["signature"] = self._sign_event(event)
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
        pattern["signature"] = self._sign_event(pattern)
        pattern["topological_signature"] = self._generate_topological_signature(pattern)

        self.vision_patterns.append(pattern)
        self.stored_patterns.append({"type": "vision_pattern", **pattern})

        sig = pattern.get("topological_signature", "")
        if sig not in self.topological_index:
            self.topological_index[sig] = []
        tag = pattern.get("detected_tags", ["unknown"])[0] if pattern.get("detected_tags") else "unknown"
        self.topological_index[sig].append(tag)

        self._link_similar_patterns(pattern)

    def _link_similar_patterns(self, pattern: Dict[str, Any]) -> None:
        current_id = pattern.get("integrity_hash", str(time.time()))
        if current_id not in self.pattern_graph:
            self.pattern_graph[current_id] = set()

        for other in self.vision_patterns[-50:]:
            if other.get("topological_signature") == pattern.get("topological_signature"):
                other_id = other.get("integrity_hash", "")
                if other_id and other_id != current_id:
                    self.pattern_graph[current_id].add(other_id)
                    if other_id not in self.pattern_graph:
                        self.pattern_graph[other_id] = set()
                    self.pattern_graph[other_id].add(current_id)

    def _generate_topological_signature(self, pattern: Dict[str, Any]) -> str:
        tags = pattern.get("detected_tags", [])
        zoom = pattern.get("zoom_level", 1.0)
        return f"t{len(tags)}_z{int(zoom)}"

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_profiles.get(user_id)

    def query_recognition_patterns(self, filters: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = self.stored_patterns[-limit:]
        if filters:
            results = [p for p in results if all(p.get(k) == v for k, v in filters.items())]
        return results

    def get_related_patterns(self, pattern_id: str, depth: int = 2) -> List[Dict[str, Any]]:
        visited = set()
        to_visit = [pattern_id]
        related = []

        for _ in range(depth):
            next_visit = []
            for pid in to_visit:
                if pid in visited:
                    continue
                visited.add(pid)
                if pid in self.pattern_graph:
                    for neighbor in self.pattern_graph[pid]:
                        if neighbor not in visited:
                            next_visit.append(neighbor)
                            for p in self.stored_patterns:
                                if p.get("integrity_hash") == neighbor:
                                    related.append(p)
                                    break
            to_visit = next_visit
        return related

    def find_shortest_path(self, start_id: str, end_id: str) -> List[str]:
        from collections import deque
        if start_id not in self.pattern_graph or end_id not in self.pattern_graph:
            return []
        queue = deque([(start_id, [start_id])])
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current == end_id:
                return path
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.pattern_graph.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return []

    def detect_communities(self) -> Dict[str, List[str]]:
        communities = {}
        for node, neighbors in self.pattern_graph.items():
            degree = len(neighbors)
            community_key = f"community_{degree // 3}"
            if community_key not in communities:
                communities[community_key] = []
            communities[community_key].append(node)
        return communities

    def infer_related_concepts(self, seed_tags: List[str], max_results: int = 10) -> List[Dict[str, Any]]:
        related = []
        for pattern in self.vision_patterns + self.stored_patterns:
            tags = pattern.get("detected_tags", [])
            if any(tag in tags for tag in seed_tags):
                related.append(pattern)
            if len(related) >= max_results:
                break
        return related

    def propagate_influence(self, start_id: str, influence_factor: float = 0.8, max_depth: int = 3) -> Dict[str, float]:
        influence = {start_id: 1.0}
        current_influence = {start_id: 1.0}

        for depth in range(max_depth):
            next_influence = {}
            for node, inf in current_influence.items():
                for neighbor in self.pattern_graph.get(node, []):
                    new_inf = inf * influence_factor
                    if neighbor not in influence or new_inf > influence[neighbor]:
                        influence[neighbor] = new_inf
                        next_influence[neighbor] = new_inf
            current_influence = next_influence
            if not current_influence:
                break
        return influence

    def cluster_patterns(self) -> Dict[str, List[str]]:
        clusters = {}
        visited = set()
        cluster_id = 0

        for node in list(self.pattern_graph.keys()):
            if node in visited:
                continue
            cluster = []
            stack = [node]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                cluster.append(current)
                for neighbor in self.pattern_graph.get(current, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
            clusters[f"cluster_{cluster_id}"] = cluster
            cluster_id += 1
        return clusters

    def predict_future_patterns(self, current_state: Dict[str, Any], steps: int = 3) -> List[Dict[str, Any]]:
        """Deeper inference: predict likely future patterns based on current graph state."""
        predictions = []
        current_tags = current_state.get("detected_tags", [])

        for _ in range(steps):
            related = self.infer_related_concepts(current_tags, max_results=5)
            if not related:
                break
            # Simple prediction: most common tags in related patterns
            tag_counts = {}
            for p in related:
                for t in p.get("detected_tags", []):
                    tag_counts[t] = tag_counts.get(t, 0) + 1
            if tag_counts:
                next_tag = max(tag_counts, key=tag_counts.get)
                predictions.append({"predicted_tag": next_tag, "confidence": tag_counts[next_tag] / len(related)})
                current_tags = [next_tag]
        return predictions

    def _signature_similarity(self, sig1: str, sig2: str) -> float:
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
            "graph_edges": sum(len(v) for v in self.pattern_graph.values()),
            "communities": len(self.detect_communities()),
            "clusters": len(self.cluster_patterns()),
            "average_cluster_size": sum(len(v) for v in self.topological_index.values()) / max(len(self.topological_index), 1)
        }

    def _calculate_human_rate(self) -> float:
        if not self.stored_patterns:
            return 0.0
        verified = sum(1 for p in self.stored_patterns if p.get("is_human_verified"))
        return verified / len(self.stored_patterns)
