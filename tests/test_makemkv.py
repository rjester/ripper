import subprocess

import pytest

from ripper.makemkv import MakeMKVClient


def test_build_args_basic():
    client = (
        MakeMKVClient("makemkvcon64.exe")
        .set_option("cache", 128)
        .set_option("messages", "-stdout")
        .enable_flag("noscan")
        .set_robot(True)
        .set_command("backup")
        .add_param("disc:0", "C:/out")
    )

    args = client.build_args()

    assert args[0] == "makemkvcon64.exe"
    # order-sensitive elements
    assert "--cache=128" in args
    assert "--messages=-stdout" in args
    assert "--noscan" in args
    assert "-r" in args
    assert "backup" in args
    assert "disc:0" in args
    assert "C:/out" in args


def test_bool_and_no_value_opts():
    client = MakeMKVClient("makemkvcon64.exe")
    client.set_option("directio", True)
    client.set_option("upnp", False)
    client.set_option("noscan", True)

    args = client.build_args()

    assert "--directio=true" in args
    assert "--upnp=false" in args
    assert "--noscan" in args


def test_run_invokes_subprocess(monkeypatch):
    client = MakeMKVClient("makemkvcon64.exe")
    client.set_option("cache", 1).set_command("info").add_param("disc:9999")

    captured = {}

    def fake_run(*f_args, **f_kwargs):
        # first positional arg is the argv list
        args_passed = f_args[0] if f_args else f_kwargs.get('args')
        captured['args'] = args_passed
        return subprocess.CompletedProcess(args=args_passed, returncode=0, stdout='ok', stderr='')

    import ripper.makemkv as mkmod
    monkeypatch.setattr(mkmod.subprocess, 'run', fake_run)

    proc = client.run(timeout=5, check=False)

    assert proc.returncode == 0
    assert proc.stdout == 'ok'
    assert captured['args'][0] == 'makemkvcon64.exe'
    assert 'info' in captured['args']
