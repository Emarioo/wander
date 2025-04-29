#!/usr/bin/python3

import os, sys, hashlib, shutil, datetime, subprocess

MODE_COMPILE_GAME = 1
MODE_RUN_WEBSITE = 2
MODE_COMPILE_INSTALLER = 3
MODE_RUN_CONTENT_SERVER = 4
MODE_DISTRIBUTE = 5
MODE_MANIFEST = 6
MODE_COMPILE_ALL = 7

def main():
    game_version = "none"
    mode = MODE_COMPILE_GAME
    channel = "release"
    path_private_key = None
    dist_dir = None
    run = False
    argi = 1
    while argi < len(sys.argv):
        arg = sys.argv[argi]
        argi += 1
        if arg == "website":
            mode = MODE_RUN_WEBSITE
        elif arg == "installer":
            mode = MODE_COMPILE_INSTALLER
        elif arg == "server":
            mode = MODE_RUN_CONTENT_SERVER
        elif arg == "all":
            mode = MODE_COMPILE_ALL
        elif arg == "dist":
            mode = MODE_DISTRIBUTE
            if argi < len(sys.argv) and not sys.argv[argi].startswith("-"):
                channel = sys.argv[argi]
                arg+=1
        elif arg == "manifest":
            mode = MODE_MANIFEST
            if argi < len(sys.argv) and not sys.argv[argi].startswith("-"):
                dist_dir = sys.argv[argi]
                argi+=1
        elif arg == "--private-key":
            if argi >= len(sys.argv):
                print("Missing path after {arg}")
                exit(1)

            path_private_key = sys.argv[argi]
            argi+=1
        elif arg == "--run":
            run = True
        else:
            print(f"Unknown argument {arg}")
            exit(1)

    if mode == MODE_COMPILE_GAME:
        compile_game()
        os.system("bin\\core.exe")
    elif mode == MODE_COMPILE_ALL:
        compile_game()
        res = os.system("btb website/src/website.btb -o bin/website.exe")
        compile_installer()
        res = os.system("btb installer/src/backend.btb -o bin/server.exe")
    elif mode == MODE_RUN_WEBSITE:
        res = os.system("btb website/src/website.btb -o bin/website.exe")
        if res == 0 and run:
            os.system("bin\\website.exe")
    elif mode == MODE_COMPILE_INSTALLER:
        compile_installer()
        if run:
            os.system("bin\\installer.exe")
    elif mode == MODE_RUN_CONTENT_SERVER:
        res = os.system("btb installer/src/backend.btb -o bin/server.exe")
        if res == 0 and run:
            os.system("bin\\server.exe")
    elif mode == MODE_MANIFEST:
        def collect_local_files(dir):
            game_files = []
            
            for folder, _, files in os.walk(dir):
                for filename in files:
                    file_path = os.path.join(folder, filename)
                    if file_path.startswith("manifest."):
                        continue
                    game_files.append((file_path[len(dir)+1:], file_path))

            return game_files

        files = collect_local_files(dist_dir)
        create_manifest(game_version, files, f"{dist_dir}/manifest.txt")
        sign_manifest(f"{dist_dir}/manifest.txt", f"{dist_dir}/manifest.sig", path_private_key)

        print(f"Created manifest in {dist_dir}")
    elif mode == MODE_DISTRIBUTE:
        compile_installer()
        compile_game()

        version = fetch_game_version()
        files = collect_game_files()
        dist_dir = f"bin/dist"

        create_manifest(version, files, f"{dist_dir}/manifest.txt")
        sign_manifest(f"{dist_dir}/manifest.txt", f"{dist_dir}/manifest.sig")

        for dst,src in files:
            full = f"{dist_dir}/{dst}"
            os.makedirs(os.path.dirname(full), exist_ok=True)
            shutil.copy(src, full)

        os.system(f"bin\\installer.exe --upload {channel} {dist_dir}")
    else: 
        assert False

def compile_game():
    res = os.system("btb src/main.btb -o bin/core.exe")
    if res != 0:
        exit(1)

def compile_installer():
    res = os.system("btb installer/src/main.btb -o bin/installer.exe")
    if res != 0:
        exit(1)

def compile_content_server():
    res = os.system("btb installer/src/backend.btb -o bin/server.exe")
    if res != 0:
        exit(1)
    
def compile_website():
    res = os.system("btb website/rc/website.btb -o bin/website.exe")
    if res != 0:
        exit(1)

def fetch_game_version():
    with open("src/const.btb") as f:
        text = f.read()
        KEYWORD = "#macro VERSION"
        at = text.find(KEYWORD)
        head = at + len(KEYWORD)

        while head < len(text):
            c = text[head]
            if c != " " and c != "\t":
                break
            head+=1

        assert text[head] == "\""
        end = text[head+1:].find("\"")

        return text[head+1:end]

    print("Failed fetching game version")
    exit(1)

def fetch_git_commit():
    proc = subprocess.run(["git","rev-parse", "--short=10", "HEAD~1"], text=True, stdout=subprocess.PIPE)
    if proc.returncode != 0:
        exit(1)

    print(f"[{proc.stdout}]")
    return proc.stdout

def collect_game_files():
    game_files = []
    game_files.append(("core.exe", "bin/core.exe"))
    # game_files.append(("game.dll", "bin/game.dll"))
    
    for folder, _, files in os.walk("assets"):
        for filename in files:
            file_path = os.path.join(folder, filename)
            game_files.append((file_path, file_path))

    return game_files

def create_manifest(game_version, game_files, output_path):
    now = datetime.datetime.now()

    text = ""
    text += f"# metadata\n"
    text += f"game_version {game_version}\n"
    text += f"date         {now.year}-{now.month:02}-{now.day:02}\n"
    text += "\n"
    text += f"# game_files\n"

    for entry_path, src_path in game_files:
        entry_path = entry_path.replace("\\","/")
        sha256 = hashlib.sha256()
        with open(src_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        text += f"{entry_path} {sha256.hexdigest()}\n"
    
    with open(output_path, 'w', encoding='utf-8') as manifest:
        manifest.write(text)

def sign_manifest(manifest, out_path, path_private_key = "private_key.pem"):
    res = os.system(f"openssl dgst -sha256 -sign {path_private_key} -out {out_path} {manifest}")
    if res != 0:
        exit(1)

if __name__ == "__main__":
    main()
