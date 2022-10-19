import signal
import sys, os
import subprocess
import time
from datetime import datetime


REACT_APP = "react"
FLASK_APP = "flask"

processes = {REACT_APP: None, FLASK_APP: None}

# env = {}
# env.update(os.environ)
# env["FLASK_APP"] = "flaskr"


def as_proper_cmd(cmd):
    return cmd
    # return cmd.split()


def log_file_of(app):
    return os.path.join("auxiliary", "logs", f"{app}_log.log")


def run_app(app, cmd, **kwargs):
    logfile = open(log_file_of(app), "w")
    logfile.write(f"\n<>-----Running the {app} app at {datetime.now()}-----<>\n\n")
    processes["react"] = subprocess.Popen(
        as_proper_cmd(cmd), stdout=logfile, shell=True, **kwargs
    )
    logfile.close()


def run_flask():
    run_app(FLASK_APP, "./auxiliary/another_wrapper_lmao")


def run_react():
    run_app(REACT_APP, "npm ci ; npm start", cwd="frontend")


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
    print()
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, gentle_signal_handler)
    run_flask()
    run_react()
    signal.pause()
