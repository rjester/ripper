# ripper
CLI to seamlessly integrate MakeMKV and HandBrake for efficient DVD ripping and encoding

## Preferred usage

Use the subcommand form. This repository enforces subcommands (e.g. `greet`) so options are only valid after the subcommand.

Local (no install):

```bash
python src/cli.py greet --name "Russ" --verbose
```

Installable (recommended for repeated use):

```powershell
# Activate project venv (Windows PowerShell)
C:\SourceCode\ripper\.venv\Scripts\Activate.ps1
# Install the package in editable mode so the `ripper` console script is available
pip install -e .
# Then run:
ripper greet --name "Russ" --verbose

Notes:
- The CLI currently requires a subcommand (e.g. `greet`).
- If you only want the minimal dependency, install `typer` into the same environment:

```powershell
pip install typer
```

# Examples

Basic usage (greet):

```bash
python src/cli.py greet --name "Russ" --verbose
# or, once installed as a console script:
ripper greet --name "Russ" --verbose
```

Examples for future ripper commands (placeholders):

```bash
# Rip a disc to MKV (placeholder example)
ripper rip --device "/dev/dvd" --output "/tmp/movie.mkv" --preset fast

# Encode an MKV using HandBrake (placeholder example)
ripper encode --input "/tmp/movie.mkv" --output "/tmp/movie-encoded.mp4" --preset "HQ" --quality 20
```

Flags

- `--name` (string): Name to greet. Default: `world`.
- `--verbose` (flag): Enable verbose output.

Note: each subcommand will document its own flags; these are the flags for `greet`.

CI (GitHub Actions)

Add a lightweight CI workflow to run linting and a CLI smoke test. Create `.github/workflows/ci.yml` with:

```yaml
name: CI

on: [push, pull_request]

jobs:
	test:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Set up Python
				uses: actions/setup-python@v4
				with:
					python-version: '3.13'
			- name: Install
				run: |
					python -m pip install --upgrade pip
					pip install -e .
			- name: Lint (optional)
				run: |
					pip install flake8
					flake8 src || true
			- name: CLI smoke test
				run: |
					# Run a simple smoke command to ensure the entrypoint works
					python src/cli.py greet --name CI --verbose
```

This workflow installs the package in editable mode and runs a quick invocation of the CLI. Extend the workflow to run unit tests, formatting, and security checks as the project grows.

If you'd like, I can also add the actual CI file and a small test harness for the CLI.
# ripper
CLI to seamlessly integrate MakeMKV and HandBrake for efficient DVD ripping and encoding

## Recommended usage

Preferred CLI form (enforced by the app):

```bash
python src/cli.py greet --name <name> --verbose
# or, after installing the package in the project venv:
ripper greet --name <name> --verbose
```

Notes:
- The CLI requires using the `greet` subcommand (future commands will follow the same pattern).
- To install dependencies into the project's virtual environment:

```powershell
C:\SourceCode\ripper\.venv\Scripts\Activate.ps1
pip install -e .
```

Or install Typer directly if you don't want to install the package:

```powershell
C:\SourceCode\ripper\.venv\Scripts\Activate.ps1
pip install typer
```
