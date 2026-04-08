# jcllc-mem-sys/README.md
# JCLLC Mem Sys SDK — Topological Memory Palace

**Pure Bit Drift + TDA Meshes + Omni Math**  
*Our open-source interpretation of MemPalace — no ChromaDB, zero external dependencies, edge-node native.*

## Architecture (Mermaid)
```mermaid
graph TD
    A[Wings] --> B[Halls]
    B --> C[Rooms]
    C --> D[Drawers.jsonl]
    D --> E[TDA Memory Mesh]
    E --> F[Bit Drift Inference]
    F --> G[Sovereign Omni Kernel (SVD)]
    G --> H[Q-Mark Thresholding]
    subgraph "Local Edge Node"
        E
    end

# JCLLC Mem Sys SDK

High-Fidelity Topological Memory Palace powered by the Omni Math Kernel. 
Engineered for Apple Silicon (M4/M1) and Slate AX / Starlink edge node local deployment.

## Architecture
Replaces legacy embedding systems with SVD Topological Data Analysis (TDA) meshes and Gamma Signal Inference. Memory nodes quantify context through Bit Drift (Feature Disagreement Score) rather than scalar similarity.

Memory state relies on:
- **L0:** Identity Manifold
- **L1:** Critical Facts (Quantum Matrix Q-Mark thresholding)
- **L2:** Room Recall (Topological state mapping)
- **L3:** Deep Search (Freedman Distance Ladder)

## Installation
```bash
pip install jcllc-mem-sys