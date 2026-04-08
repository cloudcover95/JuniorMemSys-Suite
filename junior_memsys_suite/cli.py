# junior-memsys-suite/junior_memsys_suite/cli.py
import typer
import uvicorn
from typing import Optional
from junior_memsys_suite.core.palace import MemoryPalace
from junior_memsys_suite.config import settings

app = typer.Typer(help="JCLLC Mem Sys SDK CLI — Bit Drift + TDA Memory Palace")

@app.command()
def init():
    settings.storage_path.mkdir(parents=True, exist_ok=True)
    typer.echo(f"[OK] Manifold mapped at {settings.storage_path}")

@app.command()
def mine(
    content: str = typer.Option(..., "--content", help="Raw verbatim state tensor"),
    wing: str = typer.Option("alpha", "--wing"),
    hall: str = typer.Option("main", "--hall"),
    room: str = typer.Option("buffer", "--room"),
):
    palace = MemoryPalace()
    success = palace.store(wing, hall, room, content)
    typer.echo("[SUCCESS] Tensor etched" if success else "[REJECTED] Q-Mark constraint failed")

@app.command()
def search(query: str = typer.Option(..., "--query"), wing: Optional[str] = None):
    palace = MemoryPalace()
    results = palace.semantic_search(query, wing)
    typer.echo(f"[OK] Found {len(results)} coherent states via Bit Drift.")

@app.command()
def wake_up(host: str = "0.0.0.0", port: int = 8080):
    typer.echo(f"Booting JCLLC Edge Node on {host}:{port}")
    uvicorn.run("junior_memsys_suite.server:app", host=host, port=port)

if __name__ == "__main__":
    app()