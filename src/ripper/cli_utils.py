"""
CLI utility functions for ripper commands.

This module contains shared utilities used by command modules,
keeping them separate from the main CLI argument parsing.
"""

import os
import sys
from typing import Any

# Collect deprecation warnings to print at end (avoids breaking JSON output)
_deprecated_parser_warnings = []

def find_drives() -> list[Any]:

    """Find available drives on the system.

    Returns a list of drive letters (e.g., ['C:\\', 'D:\\']) on Windows,
    or ['/'] on Unix-like systems.
    """
    drives = []
    if os.name == 'nt':
        import string
        from ctypes import windll

        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
    else:
        drives.append('/')

    return drives
