"""Lightweight wrapper for calling makemkvcon64.exe with common options.

This module provides `MakeMKVClient` which builds command-line
arguments according to the usage in `makemkv_usage.txt` and runs the
executable capturing stdout/stderr.

The wrapper is intentionally minimal and focuses on constructing
arguments correctly and executing the process via subprocess.
"""
from __future__ import annotations

import subprocess
from typing import Any, Dict, List, Optional


class MakeMKVClient:
    """Constructs and runs `makemkvcon64.exe` commands.

    Basic usage:
        client = MakeMKVClient("C:/Path/to/makemkvcon64.exe")
        client.set_option("cache", 16)
        client.set_robot(True)
        client.set_command("backup")
        client.add_param("disc:0", "C:/TargetFolder")
        proc = client.run()

    The class intentionally accepts option names without leading dashes
    (e.g. "cache", "messages", "bindip"). Use `enable_flag` to add
    flags that do not take values (e.g. "--noscan").
    """

    _NO_VALUE_OPTS = {"decrypt", "noscan"}
    _BOOL_EQUALS_OPTS = {"directio", "upnp"}

    def __init__(self, exe_path: str = "makemkvcon64.exe") -> None:
        self.exe_path = exe_path
        self._options: Dict[str, Any] = {}
        self._flags: List[str] = []
        self._robot: bool = False
        self._command: Optional[str] = None
        self._params: List[str] = []

    def set_option(self, name: str, value: Any) -> "MakeMKVClient":
        """Set an option value.

        Examples:
            set_option('cache', 16) -> --cache=16
            set_option('messages', '-stdout') -> --messages=-stdout
            set_option('directio', True) -> --directio=true
        """
        self._options[name] = value
        return self

    def enable_flag(self, flag: str) -> "MakeMKVClient":
        """Enable a standalone flag (without value), e.g. 'noscan' -> --noscan."""
        self._flags.append(flag)
        return self

    def set_robot(self, enabled: bool = True) -> "MakeMKVClient":
        """Enable or disable automation mode (-r)."""
        self._robot = bool(enabled)
        return self

    def set_command(self, command: str) -> "MakeMKVClient":
        """Set the primary command (e.g. 'mkv', 'info', 'backup', 'stream')."""
        self._command = command
        return self

    def add_param(self, *params: Any) -> "MakeMKVClient":
        """Append positional parameters (e.g. 'disc:0', target path)."""
        for p in params:
            self._params.append(str(p))
        return self

    def build_args(self) -> List[str]:
        """Return the full argument list to pass to subprocess.run."""
        args: List[str] = [self.exe_path]

        # Options with explicit formatting rules
        for name, value in self._options.items():
            if name in self._NO_VALUE_OPTS:
                if value:
                    args.append(f"--{name}")
                # if false/None, skip
                continue

            if name in self._BOOL_EQUALS_OPTS:
                # represent booleans as true/false
                if isinstance(value, bool):
                    args.append(f"--{name}={str(value).lower()}")
                else:
                    args.append(f"--{name}={value}")
                continue

            # Generic handling: include option with =value unless value is None
            if value is None:
                args.append(f"--{name}")
            else:
                args.append(f"--{name}={value}")

        # simple flags added as-is (expects names without leading dashes)
        for flag in self._flags:
            if flag.startswith("-"):
                args.append(flag)
            else:
                args.append(f"--{flag}")

        # robot short flag
        if self._robot:
            args.append("-r")

        if self._command:
            args.append(self._command)

        args.extend(self._params)
        return args

    def run(
        self,
        timeout: Optional[float] = None,
        check: bool = False,
        env: Optional[Dict[str, str]] = None,
    ) -> subprocess.CompletedProcess:
        """Execute the constructed command and return CompletedProcess.

        - Captures stdout/stderr as text.
        - Raises subprocess.TimeoutExpired on timeout.
        - If `check` is True, raises CalledProcessError on non-zero exit.
        """
        args = self.build_args()
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=check,
            env=env,
        )
        return proc


__all__ = ["MakeMKVClient"]


if __name__ == "__main__":
    print("MakeMKVClient available. Import and use in your code.")
