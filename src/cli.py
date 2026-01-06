import sys
import typer

cli = typer.Typer(invoke_without_command=False)


@cli.command()
def greet(name: str = "world", verbose: bool = False):
    if verbose:
        typer.echo("Verbose mode is on.")
    typer.echo(f"Hello, {name}!")


def main() -> None:
    """Console entrypoint.

    Enforce the subcommand-style invocation (e.g. `ripper greet ...`) and
    dispatch to the Typer app.
    """
    argv = sys.argv[1:]
    if not argv or argv[0] != "greet":
        print("Usage: ripper greet [--name NAME] [--verbose]")
        sys.exit(2)
    # Remove the 'greet' token and run the specific command handler through Typer.
    sys.argv.pop(1)
    typer.run(greet)


if __name__ == "__main__":
    main()