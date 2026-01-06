def test_automate_module_exports_cli():
    import importlib

    mod = importlib.import_module("ripper.automate_handbrake.cli")
    assert hasattr(mod, "cli")
    assert hasattr(mod, "config_show")
    assert hasattr(mod, "rip")
