"""
Ripper CLI - Command-line interface.

Usage:
    ripper /path/to/config/dir               # Analyze using config directory
    ripper /path/to/config/dir --summary     # Summary only (no HTML)
    ripper /path/to/config/dir --settings settings-2024.yaml
    ripper --help-config                     # Show detailed config documentation
"""

import argparse
from ._version import (VERSION)


def main(argv=None):
    """Entry point for the ripper CLI.

    Subcommands:
    - greet: print a greeting (uses print_hi)
    - version: print package version
    """
    parser = argparse.ArgumentParser(
        prog="ripper",
        description="A tool to rip DVDs and convert videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    greet = subparsers.add_parser("greet", help="Print a greeting")
    greet.add_argument("--name", "-n", default="PyCharm", help="Name to greet")

    # init subcommand
    init_parser = subparsers.add_parser(
        'init',
        help='Set up a new folder for the converted files'
    )
    init_parser.add_argument(
        'dir',
        nargs='?',
        default='converted-videos',
        help='Directory to initialize (default: ./converted-videos)'
    )

    # version subcommand
    subparsers.add_parser(
        "version",
        help="Show version information",
        description="Display the current version of ripper"
    )

    # decrypt subcommand
    subparsers.add_parser(
        "decrypt",
        help="Decrypt videos",
        description="Display the current version of ripper"
    )

    # convert subcommand
    subparsers.add_parser(
        "convert",
        help="Convert videos to different formats",
        description="Display the current version of ripper"
    )

    # run subcommand
    subparsers.add_parser(
        "run",
        help="Decrypt and convert videos",
        description="Display the current version of ripper"
    )

    args = parser.parse_args(argv)

    if args.command == "init":
        print("init")
    elif args.command == "version":
        print(VERSION)
    elif args.command == "decrypt":
        print("decrypt")
    elif args.command == "convert":
        print("convert")
    elif args.command == "run":
        print("run")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

