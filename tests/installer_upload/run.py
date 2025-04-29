from test_util import *
import sys, os, time, shutil, atexit

# TODO: Some flaws in test system.
#   installer returns exit code 0 on server errors (like failed AUTH).
#   if test is designed poorly we may pass.
# TODO: Server prints everything to stderr. Even 

def main():
    DEV_TOKEN = "test123"
    PORT = 7899

    # SETUP
    run(f"{GEN_GAME_FILES} dist 10")
    cd("server")
    server_proc: subprocess.Popen = run(f"{SERVER} --port {PORT}", background=True)
    with open("dev.token", "w") as f:
        f.write(DEV_TOKEN)
    cd("..")

    def cleanup():
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    atexit.register(cleanup)

    # dev.token for client uploader 
    with open("dev.token", "w") as f:
        f.write(DEV_TOKEN)

    time.sleep(0.25) # give server time to boot

    check_alive(server_proc) # server should not have stopped

    # UPLOAD
    run(f"{BUILD} manifest dist --private-key {PRIVATE_KEY}")
    run(f"{INSTALLER} --upload dev dist --ip localhost:{PORT}")

    # DOWNLOAD
    proc = run(f"{INSTALLER} --channel dev --install-dir channels --ip localhost:{PORT}", get_proc=True)

    if "WARNING" in proc.stdout:
        print("SERVER STDOUT")
        print(server_proc.stdout)
        print("SERVER END STDOUT")
        print(proc.stdout)
        exit(1)

    # print("SERVER STDOUT")
    # print(server_proc.stdout)
    # print("SERVER END STDOUT")

    server_proc.terminate()

    sys.stdout.flush()

    exit(0)

def clean():
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("server"):
        shutil.rmtree("server")
    if os.path.exists("channels"):
        shutil.rmtree("channels")
    if os.path.exists("dev.token"):
        os.remove("dev.token")

    exit(0)