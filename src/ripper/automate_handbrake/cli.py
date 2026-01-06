import sys
from pathlib import Path
import typer

from . import config as ah_config
from . import logger as ah_logger
from . import makemkv as ah_makemkv
from . import handbrake as ah_handbrake

cli = typer.Typer()


@cli.command()
def version():
    """Print version info."""
    typer.echo("ripper automate: provisional implementation")


@cli.command()
def config_show(path: Path | None = None):
    """Show the resolved configuration."""
    cfg = ah_config.load_config(path)
    for k, v in cfg.items():
        typer.echo(f"{k}: {v}")


@cli.command()
def config_migrate(path: Path | None = None):
    """Run automatic migration from legacy JSON config if present."""
    dest = ah_config.migrate_legacy_config(path)
    typer.echo(f"Migrated config to: {dest}")


@cli.command()
def list_devices(makemkv_path: str | None = None, dry_run: bool = False):
    """List optical drives detected by MakeMKV (best-effort)."""
    if dry_run:
        typer.echo("Dry-run: would list devices (makemkv_path=%s)" % makemkv_path)
        raise typer.Exit()
    drives = ah_makemkv.find_drives(makemkv_path)
    if not drives:
        typer.echo("No drives detected")
        raise typer.Exit(1)
    for d in drives:
        typer.echo(f"{d.get('Index')}: {d.get('DriveName')} - {d.get('DiscName')}")


@cli.command()
def rip(
    drive: int = 0,
    selection: str = "all",
    out_dir: Path | None = None,
    makemkv_path: str | None = None,
    dry_run: bool = False,
):
    """Rip titles from a drive using MakeMKV."""
    out_dir = out_dir or Path(ah_config.load_config().get("DefaultOutputPath"))
    if dry_run:
        typer.echo(f"Dry-run: would rip drive={drive} selection={selection} to {out_dir}")
        raise typer.Exit()
    res = ah_makemkv.rip_titles(drive, selection, str(out_dir), makemkv_path)
    typer.echo(f"Rip result: Success={res.get('Success')} Files={len(res.get('Files',[]))}")


@cli.command()
def encode(
    input_file: Path,
    output_file: Path,
    preset_file: Path | None = None,
    preset_name: str | None = None,
    container: str = "mp4",
    handbrake_path: str | None = None,
    dry_run: bool = False,
):
    """Encode a file using HandBrakeCLI."""
    if dry_run:
        typer.echo(f"Dry-run: would encode {input_file} -> {output_file} (preset={preset_name})")
        raise typer.Exit()
    res = ah_handbrake.encode(str(input_file), str(output_file), str(preset_file) if preset_file else None, preset_name, container, handbrake_path)
    typer.echo(f"Encode result: Success={res.get('Success')} ExitCode={res.get('ExitCode')}")


def main():
    # Allow invocation as module: python -m ripper.automate_handbrake.cli
    cli()


if __name__ == "__main__":
    main()
