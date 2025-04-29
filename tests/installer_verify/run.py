from test_util import *


def main():
    # SETUP
    run(f"{GEN_GAME_FILES} dist 50")
    run(f"{BUILD} manifest dist --private-key {PRIVATE_KEY}")

    # VERIFY
    run(f"{INSTALLER} --verify dist")

    exit(0)

def clean():
    import shutil, os
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    exit(0)