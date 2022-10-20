import signal
import os
import sys
import subprocess
import time
from datetime import datetime


REACT_APP = "react"
FLASK_APP = "flask"

processes = {REACT_APP: None, FLASK_APP: None}


def log_file_of(app):
    return os.path.join("auxiliary", "logs", f"{app}_log.log")


def run_app(app, cmd, **kwargs):
    processes["react"] = subprocess.Popen(cmd, shell=True, **kwargs)


def run_flask():
    run_app(FLASK_APP, "./auxiliary/flask_run_wrapper")


def run_react():
    run_app(REACT_APP, "npm start", cwd="frontend")


def interrupt_process(app):
    pr = processes[app]
    if pr:
        pr.send_signal(signal.SIGINT)


def print_mysteriously(msg, endline=False):
    print(msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    if endline:
        print()


def gentle_signal_handler(sig, frame):
    print_mysteriously("\nYou pressed Ctrl+C!", endline=True)
    print_mysteriously("Killing Flask App")
    interrupt_process(FLASK_APP)
    print("     Killed")
    print_mysteriously("Killing React App")
    interrupt_process(REACT_APP)
    print("     Killed")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, gentle_signal_handler)
    run_flask()
    # run_react()
    signal.pause()
