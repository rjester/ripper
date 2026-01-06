import subprocess
import sys


def test_greet_cli():
    p = subprocess.run([
        sys.executable,
        '-m', 'ripper.cli',
        'greet',
        '--name',
        'CI',
        '--verbose',
    ], capture_output=True, text=True)
    assert p.returncode == 0, f"CLI failed: {p.stderr}"
    assert 'Hello, CI!' in p.stdout
