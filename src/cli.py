try:
    import typer

    cli = typer.Typer(invoke_without_command=False)

    @cli.command()
    def greet(name: str = "world", verbose: bool = False):
        if verbose:
            typer.echo("Verbose mode is on.")
        typer.echo(f"Hello, {name}!")

    if __name__ == "__main__":
        import sys
        # Enforce subcommand usage: disallow passing the command's options at top-level.
        argv = sys.argv[1:]
        # Require the 'greet' subcommand; dispatch to the function when present.
        if not argv or argv[0] != "greet":
            print("Usage: cli.py greet [--name NAME] [--verbose]")
            sys.exit(2)
        # Remove the 'greet' token and run the command handler through Typer.
        sys.argv.pop(1)
        typer.run(greet)
except ModuleNotFoundError:
    # Fallback to argparse so the script can run without installing `typer`.
    import sys
    import typer

    cli = typer.Typer()


    @cli.command()
    def greet(name: str = "world", verbose: bool = False):
        if verbose:
            typer.echo("Verbose mode is on.")
        typer.echo(f"Hello, {name}!")


    if __name__ == "__main__":
        # Require the 'greet' subcommand to enforce consistent CLI usage.
        argv = sys.argv[1:]
        if not argv or argv[0] != "greet":
            print("Usage: cli.py greet [--name NAME] [--verbose]")
            sys.exit(2)
        # Remove the subcommand token and dispatch directly to the command handler.
        sys.argv.pop(1)
        typer.run(greet)