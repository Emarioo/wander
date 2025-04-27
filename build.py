#!/usr/bin/python3

import os, sys, hashlib, shutil, datetime

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
        os.system("bin\\core.exe")
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

        sign_manifest("bin/manifest.txt", "bin/manifest.sig")

        channel = "release"

        temp_dir = f"sandbox/server/{channel}"
        os.makedirs(temp_dir, exist_ok=True)
        shutil.copy("bin/manifest.txt", f"{temp_dir}/manifest.txt")
        shutil.copy("bin/manifest.sig", f"{temp_dir}/manifest.sig")
        shutil.copy("bin/core.exe", f"{temp_dir}/core.exe")

        for folder, _, files in os.walk("assets"):
            for filename in files:
                file_path = os.path.join(folder, filename)
                dst = f"{temp_dir}/{file_path}"
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(file_path, dst)

        # os.system(f"bin\\installer.exe upload {version}")
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
        entry_path = entry_path.replace("\\","/")
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        return f"{entry_path} {sha256.hexdigest()}\n"

    game_version = "wander-0.3.1"

    now = datetime.datetime.now()
    text += f"# metadata\n"
    text += f"game_version {game_version}\n"
    text += f"date         {now.year}-{now.month:02}-{now.day:02}\n"
    text += "\n"
    text += f"# game_files\n"

    text += add_file("core.exe", "bin/core.exe")
    # text += add_file("game.dll", "bin/game.dll")

    for folder, _, files in os.walk("assets"):
        for filename in files:
            file_path = os.path.join(folder, filename)
            text += add_file(file_path, file_path)
    
    with open(output_path, 'w', encoding='utf-8') as manifest:
        manifest.write(text)

def sign_manifest(manifest, out_path):
    private_key_path = "private_key.pem"
    res = os.system(f"openssl dgst -sha256 -sign {private_key_path} -out {out_path} {manifest}")
    if res != 0:
        exit(1)

if __name__ == "__main__":
    main()
