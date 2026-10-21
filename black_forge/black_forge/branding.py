"""Shared Black Forge branding used by every command-line entry point."""

import os
import sys

from rich.console import Console
from rich.panel import Panel

APP_NAME = "Black Forge"
TAGLINE = "Personal Agent OS & Marketing Framework"
VERSION = "0.1.0"
CREDIT = "Made with love Rohan Malyadri From Obscuron X Labs"
CREDIT_RICH = "Made with [red]love[/red] [bold]Rohan Malyadri[/bold] From [bold]Obscuron X Labs[/bold]"

# Windows consoles / redirected output may use a legacy code page; never crash on the emoji.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(errors="replace")
        except (ValueError, OSError):
            pass

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
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    # The .env.example placeholder doesn't count as a key
    return bool(key) and key != "your_gemini_api_key_here"


def print_missing_key():
    console.print(
        "[bold red]No Gemini API key found.[/bold red] Put "
        "[cyan]GOOGLE_API_KEY=your_key[/cyan] in the [bold].env[/bold] file in the Black Forge folder "
        "(get a key at https://aistudio.google.com/apikey), or export it in your shell."
    )
