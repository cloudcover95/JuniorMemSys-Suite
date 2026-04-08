<div align="center">
  <h1>🧬 JuniorMemSys-Suite</h1>
  <p><b>High-Fidelity Topological Memory Palace for Edge-Native AI</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]([https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT))
  [![Python >=3.9](https://img.shields.io/badge/Python->=3.9-green.svg)](https://python.org)
  [![Architecture](https://img.shields.io/badge/Architecture-Apple_Silicon_|_Linux_VM-orange.svg)]()
  [![Paradigm](https://img.shields.io/badge/Paradigm-Fullstack_Edge_AI-purple.svg)]()
</div>

## Overview
**JuniorMemSys-Suite** replaces legacy scalar vector databases (ChromaDB, FAISS) with **Topological Data Analysis (TDA) Meshes** and **Gamma Signal Inference**. Designed for Apple Silicon (M4/M1) and local network deployments, it acts as a highly efficient, deterministic, and locally sovereign memory engine for LLM workspaces and autonomous agents.

Memory context is quantified through **Bit Drift (Feature Disagreement Score)** and mathematical manifold etching, eliminating the overhead of standard similarity embeddings and SQLite WAL locking.

### 🛡️ Intellectual Property Notice
The core mathematical kinematics (`SovereignOmniKernel`) driving the SVD meshing and Q-Mark thresholds are the proprietary intellectual property of **JuniorCloud LLC**. To comply with open-source distribution while maintaining IP integrity, the math core is shipped as a protected C-Extension binary (`.so`). Raw algebraic logic is strictly isolated from this public repository.

## Architecture

```mermaid
graph TD
    A[Raw Data / Chat Tensor] --> B[Sovereign Omni Kernel]
    B --> C{Q-Mark Threshold}
    C -- "Sub-Threshold (Noise)" --> D[Discard]
    C -- "High Intensity (Action)" --> E[TDA Quartz Manifold]
    E --> F[Bit Drift Inference]
    F --> G[LLM Context Injection]
    subgraph "Sovereign Edge Node"
        B
        C
        E
    end
