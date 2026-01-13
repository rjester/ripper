"""
ripper 'decrypt' command - Decrypt video.
"""


def cmd_decrypt(args):
    """Handle the 'decrypt' subcommand.

    For now this is a small test harness that prints the parsed arguments so we
    can validate CLI parsing of MakeMKV-like options added to the decrypt
    subparser.
    """
    try:
        # Print parsed args as a simple key=value list for easy automation tests.
        d = vars(args)
    except Exception:
        # If args isn't a Namespace, just print it
        print(args)
        return

    for k in sorted(d.keys()):
        print(f"{k}={d[k]!r}")
