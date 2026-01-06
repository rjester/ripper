import sys
import typer
import sys
import typer
from ripper import cli as top_cli

# Mount existing app
cli = typer.Typer(invoke_without_command=False)

# Re-export the previous greet command to preserve behavior


@cli.command()
def greet(name: str = "world", verbose: bool = False):
    if verbose:
        typer.echo("Verbose mode is on.")
    typer.echo(f"Hello, {name}!")


# Import the automate sub-app lazily to avoid import-time side-effects
def _mount_automate():
    try:
        from ripper.automate_handbrake import cli as ah_cli
        return ah_cli
    except Exception:
        return None


def main() -> None:
    argv = sys.argv[1:]
    ah_cli = _mount_automate()
    allowed = ("greet", "automate")
    if not argv or argv[0] not in allowed:
        print("Usage: ripper <greet|automate> [subcommand args]")
        sys.exit(2)
    sub = argv[0]
    sys.argv.pop(1)
    if sub == "greet":
        typer.run(greet)
    else:
        if ah_cli is None:
            print("Automate subcommand not available")
            sys.exit(1)
        ah_cli.main()


if __name__ == "__main__":
    main()
