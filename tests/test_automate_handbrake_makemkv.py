from pathlib import Path


def test_rip_titles_builds_output(tmp_path):
    from ripper.automate_handbrake.makemkv import rip_titles

    outdir = tmp_path / "out"
    res = rip_titles(0, "1,2", str(outdir), makemkv_path="makemkvcon")
    assert isinstance(res, dict)
    assert res.get("Success") is True
    assert outdir.exists()
