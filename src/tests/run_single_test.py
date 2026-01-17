import os
import importlib.util
import pytest

# This helper script is intended to be executed directly, not imported by pytest.
# When pytest imports this file during collection it has no package context,
# which caused import errors. Skip collection to avoid that.
if __name__ != '__main__':
    pytest.skip("run_single_test is an interactive runner; skip during pytest collection", allow_module_level=True)


def _load_test_class():
    here = os.path.dirname(__file__)
    target = os.path.join(here, 'test_cli_decrypt.py')
    spec = importlib.util.spec_from_file_location('test_cli_decrypt', target)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.TestCliDecrypt


if __name__ == '__main__':
    TestCliDecrypt = _load_test_class()
    t = TestCliDecrypt()
    try:
        t.test_messages_progress_special_values()
        print('test_messages_progress_special_values: OK')
    except Exception:
        print('test_messages_progress_special_values: FAIL')
        raise
    try:
        t.test_directio_and_upnp_boolean_flags()
        print('test_directio_and_upnp_boolean_flags: OK')
    except Exception:
        print('test_directio_and_upnp_boolean_flags: FAIL')
        raise
    try:
        t.test_length_aliases_normalize_min_max()
        print('test_length_aliases_normalize_min_max: OK')
    except Exception:
        print('test_length_aliases_normalize_min_max: FAIL')
        raise

