import json
from pathlib import Path
p = Path.home() / ".juniorhome" / "os" / "lean.json"
print(json.dumps(json.loads(p.read_text()) if p.exists() else {"ok": False, "port": "JuniorMemSys-Suite", "writes": 0}))
