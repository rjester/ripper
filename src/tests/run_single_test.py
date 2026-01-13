from tests.test_cli_decrypt import TestCliDecrypt

if __name__ == '__main__':
    t = TestCliDecrypt()
    try:
        t.test_messages_progress_special_values()
        print('test_messages_progress_special_values: OK')
    except Exception as e:
        print('test_messages_progress_special_values: FAIL')
        raise
    try:
        t.test_directio_and_upnp_boolean_flags()
        print('test_directio_and_upnp_boolean_flags: OK')
    except Exception as e:
        print('test_directio_and_upnp_boolean_flags: FAIL')
        raise
    try:
        t.test_length_aliases_normalize_min_max()
        print('test_length_aliases_normalize_min_max: OK')
    except Exception as e:
        print('test_length_aliases_normalize_min_max: FAIL')
        raise

