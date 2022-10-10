import subprocess

def test_cwd_sanity():
    assert "test/bots" in subprocess.check_output(["pwd"])
