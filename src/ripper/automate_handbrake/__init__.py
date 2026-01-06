"""Automate HandBrake integration subpackage for ripper.

Expose the Typer app from `cli` so the top-level CLI can mount it.
"""

from . import cli

__all__ = ["cli"]
