import subprocess

def temp_cwd_sanity():
    assert "test/bots" in subprocess.chech_output(["pwd"])
