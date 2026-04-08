# jcllc_mem_sys/core/knowledge_graph.py
import networkx as nx
from typing import List, Tuple
from pathlib import Path
from jcllc_mem_sys.config import settings
import json

class TopologicalKnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.db_path = settings.storage_path / "kg_triples.json"
        self._load()

    def _load(self):
        if self.db_path.exists():
            with open(self.db_path, "r") as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data, directed=True, multigraph=True)

    def _save(self):
        with open(self.db_path, "w") as f:
            json.dump(nx.node_link_data(self.graph), f)

    def add_triple(self, subject: str, predicate: str, object_: str, q_mark: float):
        self.graph.add_edge(subject, object_, relation=predicate, weight=q_mark)
        self._save()

    def query(self, entity: str) -> List[Tuple[str, str, str]]:
        if entity not in self.graph:
            return []
        edges = []
        for src, dst, data in self.graph.edges(entity, data=True):
            edges.append((src, data.get("relation", ""), dst))
        return edges