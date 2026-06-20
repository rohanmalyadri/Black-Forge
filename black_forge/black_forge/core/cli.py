import typer
from rich.console import Console

app = typer.Typer(help="black_forge: Personal Agent CLI")
console = Console()

@app.command()
def setup():
    """Run initial setup for black_forge."""
    console.print("[bold green]Initializing black_forge environment...[/bold green]")
    # Setup logic will go here
    console.print("[bold blue]✓ Setup complete.[/bold blue]")

from black_forge.core.gateway import global_session_pool
from black_forge.core.engine import QueryEngine

@app.command()
def chat(prompt: str = typer.Argument(..., help="Initial message for the agent")):
    """Start a session with the QueryEngine."""
    session = global_session_pool.create_session()
    engine = QueryEngine(session)
    
    console.print(f"Starting chat with prompt: [bold cyan]{prompt}[/bold cyan]")
    response = engine.execute_loop(prompt)
    console.print(f"[bold green]black_forge:[/bold green] {response}")

if __name__ == "__main__":
    app()
