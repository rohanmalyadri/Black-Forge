import typer

from black_forge.branding import (
    APP_NAME, CREDIT, CREDIT_RICH, TAGLINE, VERSION, console,
    has_api_key, print_banner, print_footer, print_missing_key,
)

app = typer.Typer(help=f"{APP_NAME}: Personal Agent CLI. {CREDIT}")


def _version_callback(value: bool):
    if value:
        console.print(f"{APP_NAME} v{VERSION}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", callback=_version_callback, is_eager=True, help="Show the version and exit."),
):
    """Black Forge: Personal Agent CLI."""


@app.command()
def setup():
    """Run initial setup for Black Forge."""
    print_banner()
    console.print(f"[bold green]Initializing {APP_NAME} environment...[/bold green]")
    from black_forge.core.memory import MemoryManager
    memory = MemoryManager()
    console.print(f"Config directory: [cyan]{memory.config_dir}[/cyan]")
    if has_api_key():
        console.print("[green]✓ Gemini API key detected.[/green]")
    else:
        print_missing_key()
    console.print("[bold blue]✓ Setup complete.[/bold blue]")
    print_footer()


@app.command()
def about():
    """Show information about Black Forge."""
    print_banner()
    console.print(
        f"{APP_NAME} v{VERSION}: {TAGLINE}.\n"
        "A terminal agent that reasons and acts with tools (file I/O and a\n"
        "Docker-sandboxed shell), plus the AutoReason marketing-copy optimizer.\n"
    )
    console.print(CREDIT_RICH)


@app.command()
def chat(prompt: str = typer.Argument(..., help="Initial message for the agent")):
    """Start a session with the QueryEngine."""
    print_banner()
    if not has_api_key():
        print_missing_key()
        raise typer.Exit(code=1)

    from black_forge.core.gateway import global_session_pool
    from black_forge.core.engine import QueryEngine

    session = global_session_pool.create_session()
    engine = QueryEngine(session)

    console.print(f"Starting chat with prompt: [bold cyan]{prompt}[/bold cyan]")
    try:
        response = engine.execute_loop(prompt)
        console.print(f"[bold green]{APP_NAME}:[/bold green] {response}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    finally:
        global_session_pool.close_session(session.session_id)
        print_footer()


if __name__ == "__main__":
    app()
