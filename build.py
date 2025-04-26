#!/usr/bin/python3

import os, sys, hashlib

MODE_COMPILE_GAME = 1
MODE_RUN_WEBSITE = 2
MODE_COMPILE_INSTALLER = 3
MODE_RUN_CONTENT_SERVER = 4
MODE_DISTRIBUTE = 5

def main():
    version = ""
    mode = MODE_COMPILE_GAME
    argi = 1
    while argi < len(sys.argv):
        arg = sys.argv[argi]
        argi += 1
        if arg == "web":
            mode = MODE_RUN_WEBSITE
        elif arg == "installer":
            mode = MODE_COMPILE_INSTALLER
        elif arg == "server":
            mode = MODE_RUN_CONTENT_SERVER
        elif arg == "dist":
            mode = MODE_DISTRIBUTE
        else:
            if mode == MODE_DISTRIBUTE:
                if version is None:
                    version = arg
                else:
                    print(f"Version already specified")    
            else:
                print(f"Unknown argument {arg}")
                exit(1)

    if mode == MODE_COMPILE_GAME:
        compile_game()
        os.system("bin/core.exe")
    elif mode == MODE_RUN_WEBSITE:
        res = os.system("btb website/src/website.btb -o bin/website.exe")
        if res == 0:
            os.system("bin\\website.exe")
    elif mode == MODE_COMPILE_INSTALLER:
        compile_installer()
        os.system("bin\\installer.exe")
    elif mode == MODE_RUN_CONTENT_SERVER:
        res = os.system("btb installer/src/backend.btb -o bin/server.exe")
        if res == 0:
            os.system("bin\\server.exe")
    elif mode == MODE_DISTRIBUTE:
        compile_installer()
        compile_game()

        create_manifest("bin/manifest.txt")

        os.system(f"bin\\installer.exe upload {version}")
    else: 
        assert False

def compile_installer():
    res = os.system("btb installer/src/main.btb -o bin/installer.exe")
    if res != 0:
        exit(1)

def compile_game():
    res = os.system("btb src/main.btb -o bin/core.exe")
    if res != 0:
        exit(1)

def create_manifest(output_path):
    text = ""
    
    def add_file(entry_path, path):
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        text.append(f"{entry_path} {sha256.hexdigest()}\n")

    add_file("core.exe", "bin/core.exe")
    add_file("game.dll", "bin/game.dll")

    for folder, _, files in os.walk("assets"):
        for filename in files:
            file_path = os.path.join(folder, filename)
            print(file_path)
            add_file(file_path, file_path)
    
    with open(output_path, 'w', encoding='utf-8') as manifest:
        manifest.write(text)

if __name__ == "__main__":
    main()