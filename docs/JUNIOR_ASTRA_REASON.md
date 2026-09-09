JuniorLLM `adaptations/astra_reason/memsys_bridge.py` will call `junior_memsys.put` if this package is on PYTHONPATH.
Otherwise it uses an in-tree bit-drift palace so edge nodes stay offline.
Astra-class reasoning stand-in lives in JuniorLLM, not here.
