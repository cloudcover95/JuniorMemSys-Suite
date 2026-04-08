# JuniorMemSys Suite

**High-fidelity Topological Memory Palace SDK**  
*Bit Drift + TDA Meshes + Sovereign Omni Math Kernel*

Lossless • Edge-first • Apple Silicon M4 native • No ChromaDB • Fully local

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![M4 Optimized](https://img.shields.io/badge/Apple%20Silicon-M4%20Ready-orange)

## Overview

JuniorMemSys Suite is a **production-grade topological memory system** that replaces traditional vector databases with **TDA meshes** and **Bit Drift inference**. It stores raw verbatim content with zero summarization loss and uses advanced mathematical inference (Sovereign Omni Math) for retrieval.

Perfect for long-term AI memory, agent memory layers, local RAG, and edge deployment.

## Quick Start (VSCodium + M4)

cd /

# Activate or create venv
source .venv/bin/activate   # or: python3.11 -m venv .venv && source .venv/bin/activate

# Install with all features
pip install -e ".[dev,playground,benchmarks]"

# Initialize the memory palace
junior-memsys init

# Launch the interactive TDA Sandbox
streamlit run playground/app.py
Features

Raw verbatim storage (Wings → Halls → Rooms → Drawers)
Bit Drift inference + Freedman Ladder distances
Live parameter tuning (etch threshold, variance retention, mesh capacity)
HF dataset ingestion (llm-math and more)
Knowledge Graph with temporal triples
Scalability testing pipelines
Benchmarks vs traditional vector DBs
MCP-compatible FastAPI server

Industry Standard Pipelines Included

PipelinePurposeCommand / LocationDataset MiningHF + custom dataset ingestionpipelines/dataset_miner.pyBatch IngestionLarge-scale JSONL/Parquet importpipelines/batch_ingest.pyScaling & BenchmarkingPerformance testing at 10k+ recordsbenchmarks/scaling_test.pyLongMemEval-style QAFull retrieval + generation + scoringbenchmarks/longmem_eval.py (coming)Seeding & Demo DataPre-populate palace + KGBuilt into Streamlit dashboard
Commands
Bashjunior-memsys init
junior-memsys mine --content "your text here"
junior-memsys search --query "machine learning optimization"
junior-memsys wake-up          # Start FastAPI MCP server
Project Structure
textJuniorMemSys-Suite/
├── junior_memsys_suite/      # Main package
├── playground/               # Streamlit TDA Sandbox
├── pipelines/                # Data ingestion pipelines
├── benchmarks/               # Scaling & QA benchmarks
├── tests/                    # Unit tests
├── .github/workflows/        # CI/CD
├── Dockerfile + docker-compose
└── pyproject.toml
Roadmap

Incremental indexing & file watching
PDF / document support
Full LongMemEval QA benchmark suite
Knowledge Graph visualization in UI
Ollama / local LLM integration for RAG


Made with ❤️ by JuniorCloud LLC
Optimized for Apple Silicon M4 and edge deployment.
Star ⭐ if you're building local AI memory systems!
