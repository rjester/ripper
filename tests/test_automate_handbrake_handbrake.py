from pathlib import Path


def test_encode_stub_returns_log(tmp_path, monkeypatch):
    from ripper.automate_handbrake import handbrake, external

    inp = tmp_path / "in.mkv"
    out = tmp_path / "out.mp4"
    inp.write_text("dummy")

    # Patch external.run_with_logs to avoid launching real HandBrakeCLI
    def fake_run_with_logs(cmd, cwd, out_log, err_log):
        class P:
            def poll(self):
                return 0
            def wait(self):
                return 0
        # create empty logs
        out_log.write_text("")
        err_log.write_text("")
        return P()

    def fake_monitor_progress(proc, out_log, err_log, parser=None, on_event=None, poll_ms=500):
        return 0, "", []

    monkeypatch.setattr(external, "run_with_logs", fake_run_with_logs)
    monkeypatch.setattr(external, "monitor_progress", fake_monitor_progress)

    res = handbrake.encode(str(inp), str(out), preset_file=None, preset_name=None, container='mp4', handbrake_path='HandBrakeCLI')
    assert isinstance(res.get("Success"), bool)
    assert "Log" in res
