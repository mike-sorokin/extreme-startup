import subprocess

def test_cwd_sanity():
    assert "test/bots" in subprocess.chech_output(["pwd"])
