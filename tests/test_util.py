import os, sys, subprocess, platform

py = "python " if platform.system() == "Windows" else "python3 "
INSTALLER = os.path.abspath("../../bin/installer")
SERVER = os.path.abspath("../../bin/server")
GEN_GAME_FILES = py + os.path.abspath("../gen_game_files.py")
BUILD = py + os.path.abspath("../../build.py")

PRIVATE_KEY = "../../private_key.pem"

def cd(path):
    path = os.path.abspath(path)
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

def run(cmd: str, background = False, get_proc=False):
    sp = cmd.split(" ", 1)
    # windows requires ..\..\bin\installer (forward slashes don't work)
    sp[0] = sp[0].replace("/", "\\")
    cmd = " ".join(sp)
    print(f"\033[0;30m{cmd}\033[0m")
    sys.stdout.flush()

    if background:
        return subprocess.Popen(cmd.split(" "), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # return subprocess.Popen(cmd.split(" "))
    else:
        proc = subprocess.run(cmd.split(" "), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # proc = subprocess.run(cmd.split(" "))
        if get_proc:
            return proc

        print(proc.stdout)
        if proc.returncode != 0:
            exit(1)

def check_alive(proc):
    proc.poll()
    if proc.returncode is not None:
        proc.terminate()
        print(proc.stdout.read())
        exit(1)