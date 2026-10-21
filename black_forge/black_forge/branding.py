"""Shared Black Forge branding used by every command-line entry point."""

import os

from rich.console import Console
from rich.panel import Panel

APP_NAME = "Black Forge"
TAGLINE = "Personal Agent OS & Marketing Framework"
VERSION = "0.1.0"
CREDIT = "Made with love Rohan Malyadri From Obscuron X Labs"
CREDIT_RICH = "Made with [red]love[/red] [bold]Rohan Malyadri[/bold] From [bold]Obscuron X Labs[/bold]"

console = Console()


def print_banner(subtitle: str = TAGLINE):
    console.print(Panel.fit(
        f"[bold white]🌌 {APP_NAME.upper()}[/bold white]\n[dim]{subtitle}[/dim]",
        border_style="magenta",
    ))


def print_footer():
    console.print(f"\n[dim]{APP_NAME} v{VERSION} · {CREDIT_RICH}[/dim]")


def has_api_key() -> bool:
    from dotenv import load_dotenv
    load_dotenv()
    return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))


def print_missing_key():
    console.print(
        "[bold red]No Gemini API key found.[/bold red] Create a [bold].env[/bold] file with "
        "[cyan]GOOGLE_API_KEY=your_key[/cyan] (get one at https://aistudio.google.com/apikey) "
        "or export it in your shell."
    )
