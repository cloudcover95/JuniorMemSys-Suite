JuniorMemSys-Suite v0.4.0Sovereign Topological Memory Palace SDK Apple Silicon Native · MLX-first · TDA + SVD · Bit Drift Inference · MCP ReadyJuniorMemSys-Suite is a production-grade topological memory system that replaces traditional vector databases with TDA meshes and Bit Drift inference. It stores raw verbatim content with zero summarization loss and utilizes a sovereign, edge-optimized mathematical kernel for high-fidelity retrieval.✨ Core FeaturesMLX-First Sovereign Encoder — Native Apple Silicon acceleration (MLX → MPS → Crypto fallback).Topological Memory Palace — TDA + SVD quantization running in a hierarchical Wing → Hall → Room structure.Bit Drift Inference — Replaces high-overhead cosine similarity with mean Feature Disagreement Scores (FDS).Cryptographic Provenance — SHA-256 chain-of-custody and integrity auditing on every stored memory node.Model Context Protocol (MCP) — Native support for Cursor, Claude Desktop, and local LLM agent tool-calling.Enterprise Audit Engine — Built-in benchmarking for throughput (RPS) and retrieval latency verification.TrueDepth / ARKit Bridge — gRPC integration for iPhone/iPad spatial memory and LiDAR mesh ingestion.🚀 Quick Start (M4 Deployment)1. Minimal InstallBashgit clone https://github.com/cloudcover95/JuniorMemSys-Suite.git
cd JuniorMemSys-Suite
pip install -e ".[dev,playground,benchmarks]"
2. Bootstrap the NodeThe omega_boot.sh script handles environment alignment and target service initialization.Bash./omega_boot.sh --ui          # Launch Streamlit / Gradio TDA Sandbox
./omega_boot.sh --grpc        # Start gRPC receiver for Swift TrueDepth/ARKit
./omega_boot.sh --web         # Start FastAPI MCP / WebRTC bridge
🛠 Architecture & Directory TreePlaintextJuniorMemSys-Suite/
├── 📦 junior_memsys_suite/          # Core installable SDK
│   ├── core/                        # TDA Engine & Math Kernels
│   │   ├── palace.py                # MemoryPalace logic (Provenance + Storage)
│   │   ├── tda_mesh.py              # SVD + Bit Drift Manifolds
│   │   ├── encoder.py               # MLX-Native Sovereign Encoder
│   │   └── audit.py                 # Enterprise Integrity & Benchmark Engine
│   └── pipelines/                   # Data integration layer (DatasetMiner, Chunker)
├── 🖥️ playground/                   # Streamlit Dashboard & Globe Brain Viz
├── 🔬 benchmarks/                    # LongMemEval QA & Scaling Tests
├── 🛠️ scripts/                       # Harvester, Kernel Builders, and Seeders
└── server.py                        # MCP Protocol / FastAPI Server
⚖️ Technical BaselineJuniorMemSys utilizes Bit Drift instead of cosine similarity. Tensors are projected via SVD and quantized to a $\pm 1$ binary signature. Retrieval computes the mean Feature Disagreement Score:$$\text{FDS}(q, i) = \frac{1}{d} \sum_{j=1}^{d} \frac{|\sigma_q^j - \sigma_i^j|}{2}$$Storage is gated by the Q-Mark (Sovereign Omni Math Kernel), ensuring only high-signal data etches the mesh:$$\text{Q-Mark} = \text{clip}\!\left(\frac{|z| \cdot \rho}{1 + |\nu|} - |\delta| \cdot \hbar, \; 0, \; 1\right)$$📋 Industry Standard Usage1. Semantic Storage (Provenance Enabled)Pythonfrom junior_memsys_suite.core.palace import MemoryPalace
palace = MemoryPalace()

palace.store(
    wing="alpha", 
    hall="directives", 
    room="root_node",
    content="Optimize for power-efficient, logic-dense engineering.",
    z_score=2.5
)
2. MCP Tool IntegrationJuniorMemSys serves as a native tool for Claude or Cursor. Connect to the local node:GET http://localhost:8000/mcp/tools3. Server Integrity AuditProve data consistency across the manifold:Bash# Run via CLI
junior-memsys audit --wing alpha
🗺 Roadmap (v0.5+)Incremental Indexing: Automated file-watching and delta-etching.Distributed Swarm: Local mesh synchronization across multi-agent clusters (Orange Pi/Linux).Native Swift SDK: Direct ARKit → MemoryPalace integration for spatial computing.BitNet-1.58b Integration: Topological control layers for ternary LLM inference.🛡 License & PhilosophyLicensed under Apache 2.0 / MIT.JuniorMemSys-Suite is built on the belief that AI memory should be local, verifiable, and topology-aware. While frontier cloud models focus on scale, we focus on the mathematical precision of the edge.JuniorCloud LLC • 2026 Made with precision on Apple Silicon.Star the repo if you're building sovereign, local-first AI systems! ⭐
