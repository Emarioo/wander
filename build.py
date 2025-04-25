#!/usr/bin/python3
import os, sys

MODE_COMPILE_GAME = 1
MODE_RUN_SERVER = 2

def main():
    mode = MODE_COMPILE_GAME
    argi = 1
    while argi < len(sys.argv):
        arg = sys.argv[argi]
        argi += 1
        if arg == "server":
            mode = MODE_RUN_SERVER
        else:
            print(f"Unknown argument {arg}")
            exit(1)

    if mode == MODE_COMPILE_GAME:
        os.system("btb src/main.btb -r")
    elif mode == MODE_RUN_SERVER:
        os.system("btb website/src/website.btb -o bin/website.exe")
        os.system("bin\\website.exe")

if __name__ == "__main__":
    main()