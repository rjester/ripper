import os
import runpy
import sys

# simulate running the package as a module with "greet" argument
# set argv to a program name + the command so argparse sees the command
sys.argv = [sys.argv[0], "version"]

# run the module as __main__ so its CLI entry runs normally
try:
    runpy.run_module("ripper.cli", run_name="__main__")
except SystemExit as e:
    # propagate the exit code if the CLI calls sys.exit(...)
    raise
