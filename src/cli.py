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
    import argparse
    import sys

    def greet(name: str = "world", verbose: bool = False):
        if verbose:
            print("Verbose mode is on.")
        print(f"Hello, {name}!")

    if __name__ == "__main__":
        argv = sys.argv[1:]
        # Require the 'greet' subcommand for the fallback as well.
        if not argv or argv[0] != "greet":
            print("Usage: cli.py greet [--name NAME] [--verbose]")
            sys.exit(2)
        argv = argv[1:]
        parser = argparse.ArgumentParser(prog="cli.py greet")
        parser.add_argument("--name", default="world")
        parser.add_argument("--verbose", action="store_true")
        args = parser.parse_args(argv)
        greet(args.name, args.verbose)