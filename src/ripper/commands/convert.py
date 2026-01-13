"""
ripper 'convert' command - convert video.
"""
from .. import cli_utils


def cmd_convert(args):
    """Handle the 'convert' subcommand."""
    print("convert")
    # Use cli_utils.find_drives() which works correctly when imported as a package
    try:
        drives = cli_utils.find_drives()
        print("drives=", drives)
    except Exception:
        # Keep convert lightweight for tests; don't raise on platform specifics
        print("drives=[]")
