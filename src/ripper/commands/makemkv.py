"""Convenience CLI wrapper around `MakeMKVClient`.

This command provides a simple mapping of many options from
`makemkv_usage.txt` to the `MakeMKVClient` wrapper. It is intended
for interactive use or for quick scripting where you don't want to
manually build the argument list.

Example:
    python -m ripper.commands.makemkv --exe "C:/Program Files/MakeMKV/makemkvcon64.exe" \
        --cache 16 -r backup disc:0 C:/rips
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from ripper.makemkv import MakeMKVClient


def _parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    v = value.lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    raise argparse.ArgumentTypeError("expected a boolean value (true/false)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run makemkvcon via MakeMKVClient wrapper")
    p.add_argument("--exe", default="makemkvcon64.exe", help="Path to makemkvcon64 executable")
    p.add_argument("--messages", help="--messages option value (e.g. -stdout)")
    p.add_argument("--progress", help="--progress option value (e.g. -same)")
    p.add_argument("--debug", nargs="?", const="", help="--debug[=file]")
    p.add_argument("--directio", type=_parse_bool, help="--directio=true/false")
    p.add_argument("--noscan", action="store_true", help="--noscan")
    p.add_argument("--cache", type=int, help="--cache=size (MB)")
    p.add_argument("--upnp", type=_parse_bool, help="--upnp=true/false")
    p.add_argument("--bindip", help="--bindip=address")
    p.add_argument("--bindport", type=int, help="--bindport=port")
    p.add_argument("--decrypt", action="store_true", help="--decrypt")
    p.add_argument("--minlength", type=int, help="--minlength=seconds")
    p.add_argument("-r", "--robot", action="store_true", help="-r / --robot automation mode")

    # primary command and remaining params
    p.add_argument("command", help="makemkvcon command (mkv | info | backup | stream | etc.)")
    p.add_argument("params", nargs=argparse.REMAINDER, help="Positional parameters for the command")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    client = MakeMKVClient(str(args.exe))

    if args.messages:
        client.set_option("messages", args.messages)
    if args.progress:
        client.set_option("progress", args.progress)
    if args.debug is not None:
        # If provided as bare --debug, args.debug == '' (const); pass True to enable
        client.set_option("debug", args.debug or True)
    if args.directio is not None:
        client.set_option("directio", args.directio)
    if args.noscan:
        client.set_option("noscan", True)
    if args.cache is not None:
        client.set_option("cache", args.cache)
    if args.upnp is not None:
        client.set_option("upnp", args.upnp)
    if args.bindip:
        client.set_option("bindip", args.bindip)
    if args.bindport is not None:
        client.set_option("bindport", args.bindport)
    if args.decrypt:
        client.set_option("decrypt", True)
    if args.minlength is not None:
        client.set_option("minlength", args.minlength)

    client.set_robot(bool(args.robot))
    client.set_command(args.command)

    # params comes from REMAINDER, may include leading '--' separators; strip leading '--' if present
    params: List[str] = []
    if args.params:
        # argparse.REMAINDER preserves everything; if first element is '--' drop it
        p = list(args.params)
        if p and p[0] == "--":
            p = p[1:]
        params = p
    if params:
        client.add_param(*params)

    try:
        proc = client.run()
    except Exception as exc:
        print(f"Failed to run makemkv: {exc}", file=sys.stderr)
        return 2

    # Forward stdout/stderr
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
