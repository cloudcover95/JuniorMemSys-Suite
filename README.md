# JuniorMemSys-Suite

**Current State**

Started actual integration with the calling system from JuniorHome.

Added `src/recognition/call_pattern_store.py` — a dedicated store for recognition patterns derived from DigitalCallManager events.

This enables long-term memory of voice verification patterns, user profiles from repeated calls, and topological analysis of calling behavior.

The store is designed to be used via the MemoryBackend in JuniorHome's DigitalCallManager and SHEEPMemory.

Future work: Full TDA/persistence integration for complex pattern recognition across call data.