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


# Helper validators for MakeMKV-style special file names
def _validate_special_file(val: str, allowed_specials: set):
    if isinstance(val, str) and val.startswith("-") and val not in allowed_specials:
        raise argparse.ArgumentTypeError(
            f"Invalid special value {val!r}; allowed: {', '.join(sorted(allowed_specials))}"
        )
    return val


def _messages_type(val: str):
    allowed = {"-stdout", "-stderr", "-null"}
    return _validate_special_file(val, allowed)


def _progress_type(val: str):
    allowed = {"-stdout", "-stderr", "-null", "-same"}
    return _validate_special_file(val, allowed)


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
    decrypt_parser = subparsers.add_parser(
        "decrypt",
        help="Decrypt videos",
        description="Decrypt (rip) discs or images using MakeMKV-like options"
    )

    # Device / input
    decrypt_parser.add_argument(
        "-d", "--device",
        dest="device",
        help="Optical device (e.g. /dev/sr0) or path to image/file to read from"
    )

    # Output
    decrypt_parser.add_argument(
        "-o", "--output",
        dest="output",
        default='.',
        help="Output directory for decrypted files (default: current directory)"
    )

    # Title selection
    decrypt_parser.add_argument(
        "-t", "--title",
        dest="title",
        type=int,
        help="Title number to decrypt (integer)"
    )
    decrypt_parser.add_argument(
        "--titles",
        dest="titles",
        nargs='+',
        type=int,
        help="One or more title numbers to decrypt (space-separated)"
    )

    # Length / duration filters
    # Length/duration flags (aliases for legacy names are registered later)

    # Scanning / behavior: mutually exclusive --scan / --noscan
    scan_group = decrypt_parser.add_mutually_exclusive_group()
    scan_group.add_argument(
        "--noscan",
        dest="noscan",
        action="store_true",
        help="Do not scan the input device for available titles"
    )
    scan_group.add_argument(
        "--scan",
        dest="scan",
        action="store_true",
        help="Force a fresh scan of the input device"
    )

    # Chapters, audio, subtitles
    decrypt_parser.add_argument(
        "--chapters",
        dest="chapters",
        nargs='+',
        help="Chapter ranges to extract (e.g., 1-3 or 5)"
    )
    decrypt_parser.add_argument(
        "--audio",
        dest="audio",
        nargs='+',
        help="Select audio tracks (indexes or language codes)"
    )
    decrypt_parser.add_argument(
        "--subtitle", "--subtitles",
        dest="subtitles",
        nargs='+',
        help="Select subtitle tracks (indexes or language codes)"
    )
    decrypt_parser.add_argument(
        "--lang",
        dest="lang",
        help="Preferred audio language (e.g., en)"
    )

    # Cookies / network options
    decrypt_parser.add_argument(
        "--cookies",
        dest="cookies",
        help="Path to cookies file (useful for network sources)"
    )

    # MakeMKV general options (from usage.txt)
    decrypt_parser.add_argument(
        "--messages",
        dest="messages",
        type=_messages_type,
        default='-stdout',
        help=("Output all messages to file. Special values: -stdout, -stderr, -null. "
              "Default: -stdout")
    )
    decrypt_parser.add_argument(
        "--progress",
        dest="progress",
        type=_progress_type,
        default=None,
        help=("Output all progress messages to file. Special values: -stdout, -stderr, -null, -same. "
              "Use -same to use the same file as --messages. Default: no output")
    )
    decrypt_parser.add_argument(
        "--debug",
        dest="debug",
        nargs='?',
        help=("Enable debug messages and optionally provide a debug file. "
              "If not provided, program preferences are used.")
    )

    # directio: mutually exclusive boolean flags --directio / --no-directio
    directio_group = decrypt_parser.add_mutually_exclusive_group()
    directio_group.add_argument(
        "--directio",
        dest="directio",
        action="store_true",
        default=None,
        help="Enable direct disc access (overrides program preferences)"
    )
    directio_group.add_argument(
        "--no-directio",
        dest="directio",
        action="store_false",
        help="Disable direct disc access (overrides program preferences)"
    )

    decrypt_parser.add_argument(
        "--cache",
        dest="cache",
        type=int,
        help=("Size of read cache in megabytes used by MakeMKV. "
              "Recommended: 128 for streaming, 512 for DVD, 1024 for Blu-ray.")
    )

    # Streaming options
    # upnp: mutually exclusive boolean flags --upnp / --no-upnp
    upnp_group = decrypt_parser.add_mutually_exclusive_group()
    upnp_group.add_argument(
        "--upnp",
        dest="upnp",
        action="store_true",
        default=None,
        help="Enable UPNP streaming (overrides program preferences)"
    )
    upnp_group.add_argument(
        "--no-upnp",
        dest="upnp",
        action="store_false",
        help="Disable UPNP streaming (overrides program preferences)"
    )
    decrypt_parser.add_argument(
        "--bindip",
        dest="bindip",
        help="IP address to bind the streaming/web server"
    )
    decrypt_parser.add_argument(
        "--bindport",
        dest="bindport",
        type=int,
        default=51000,
        help="Port number to bind the web server (default: 51000)"
    )

    # Backup / conversion options
    decrypt_parser.add_argument(
        "--decrypt",
        dest="decrypt_streams",
        action="store_true",
        help="Decrypt stream files during backup"
    )
    # Support both --min-length and legacy --minlength (normalize to min_length)
    decrypt_parser.add_argument(
        "--minlength",
        "--min-length",
        dest="min_length",
        type=int,
        help="Minimum title length in seconds (alias: --min-length)"
    )
    # Provide an alias for max-length
    decrypt_parser.add_argument(
        "--maxlength",
        "--max-length",
        dest="max_length",
        type=int,
        help="Maximum title length in seconds (alias: --max-length)"
    )
    # Provide aliases for duration flags
    decrypt_parser.add_argument(
        "--minduration",
        "--min-duration",
        dest="min_duration",
        type=int,
        help="Minimum duration in seconds (alias: --min-duration)"
    )
    decrypt_parser.add_argument(
        "--maxduration",
        "--max-duration",
        dest="max_duration",
        type=int,
        help="Maximum duration in seconds (alias: --max-duration)"
    )

    # Automation options
    decrypt_parser.add_argument(
        "-r", "--robot",
        dest="robot",
        action="store_true",
        help=("Enables automation (robot) mode. Outputs line-based, quoted, escaped strings. "
              "Recommended for scripting/automation.")
    )

    # Advanced output / control
    decrypt_parser.add_argument(
        "--decrypt-to",
        dest="decrypt_to",
        help="Explicit path or device to write decrypted output to"
    )
    decrypt_parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Overwrite existing output files"
    )
    decrypt_parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Show actions without performing them"
    )

    # Logging / performance
    decrypt_parser.add_argument(
        "--verbose", "-v",
        dest="verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv)"
    )
    decrypt_parser.add_argument(
        "--threads",
        dest="threads",
        type=int,
        default=1,
        help="Number of worker threads to use for post-processing (default: 1)"
    )
    decrypt_parser.add_argument(
        "--no-subtitles",
        dest="no_subtitles",
        action="store_true",
        help="Do not extract subtitles"
    )
    decrypt_parser.add_argument(
        "--no-audio",
        dest="no_audio",
        action="store_true",
        help="Do not extract audio tracks"
    )
    decrypt_parser.add_argument(
        "--scan-timeout",
        dest="scan_timeout",
        type=int,
        help="Timeout in seconds for scanning operations"
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

    # makemkv convenience wrapper subcommand - forward remaining args
    makemkv_parser = subparsers.add_parser(
        "makemkv",
        help="Run makemkvcon via the bundled MakeMKVClient wrapper",
        description="Convenience wrapper around makemkvcon64.exe"
    )
    makemkv_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to makemkv wrapper")

    args = parser.parse_args(argv)

    if args.command == "greet":
        # simple greeting handler
        name = getattr(args, "name", "PyCharm")
        print(f"Hello, {name}!")
        return

    if args.command == "init":
        from .commands import cmd_init
        cmd_init(args)
    elif args.command == "version":
        print(VERSION)
    elif args.command == "decrypt":
        from .commands import cmd_decrypt
        cmd_decrypt(args)
    elif args.command == "makemkv":
        # forward remaining argv to the makemkv command module
        from .commands import makemkv as _makemkv
        # args.args is the list after the subcommand; pass as argv to makemkv.main
        ret = _makemkv.main(args.args if getattr(args, 'args', None) else None)
        # if makemkv.main returned an exit code, propagate it
        if isinstance(ret, int) and ret != 0:
            import sys

            sys.exit(ret)
    elif args.command == "convert":
        from .commands import cmd_convert
        cmd_convert(args)
    elif args.command == "run":
        from .commands import cmd_run
        cmd_run(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

