import ast
import pytest

from ripper import cli


def _run_decrypt_and_parse(argv, capsys):
    # Run the CLI and capture stdout using pytest's capsys fixture
    cli.main(['decrypt'] + argv)
    captured = capsys.readouterr()
    out_lines = captured.out.strip().splitlines()
    parsed = {}
    for line in out_lines:
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        try:
            parsed[k] = ast.literal_eval(v)
        except Exception:
            parsed[k] = v.strip()
    return parsed


def test_messages_progress_special_values(capsys):
    parsed = _run_decrypt_and_parse(['--messages=-stdout', '--progress=-same'], capsys)
    assert parsed.get('messages') == '-stdout'
    assert parsed.get('progress') == '-same'


def test_directio_and_upnp_boolean_flags(capsys):
    parsed = _run_decrypt_and_parse(['--directio', '--upnp'], capsys)
    assert parsed.get('directio') is True
    assert parsed.get('upnp') is True


def test_length_aliases_normalize_min_max(capsys):
    parsed = _run_decrypt_and_parse(['--minlength', '30', '--maxlength', '120'], capsys)
    assert parsed.get('min_length') == 30
    assert parsed.get('max_length') == 120
