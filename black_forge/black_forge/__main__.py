"""Allows `python -m black_forge ...` as a fallback to the `s` / `black-forge` commands."""
from black_forge.core.cli import app

app(prog_name="black-forge")
