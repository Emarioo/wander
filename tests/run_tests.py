#!/usr/bin/python3
import os, sys, subprocess, importlib, platform

this_dir = os.path.dirname(__file__)
if this_dir not in sys.path:
    sys.path.append(this_dir)

verbose = False
clean = False
filters = []
test_name = None

argi = 1
while argi < len(sys.argv):
    arg = sys.argv[argi]
    argi+=1
    if arg == "--verbose":
        verbose = True
    elif arg == "--clean":
        clean = True
    elif arg == "-f" or arg == "--filter":
        if argi >= len(sys.argv):
            print(f"Missing test name after {arg}")
            exit(1)
        filters.append(sys.argv[argi])
        argi+=1
    else:
        test_name = arg

if test_name is not None:
    cwd = this_dir+"/"+test_name
    print(f"\033[0;30mcd {cwd}\033[0m")
    os.chdir(cwd)
    spec = importlib.util.spec_from_file_location("test_run_module", "run.py")
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    if clean:
        test_module.clean()
    else:
        test_module.main()

    exit(0)

class TestResult:
    def __init__(self, name, result):
        self.name = name
        self.passed = result

def run_py(cmd):
    return subprocess.run(["python" if platform.system() == "Windows" else "python3"] + cmd.split(" "), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # return subprocess.run(["python" if platform.system() == "Windows" else "python3"] + cmd.split(" "))

results = []
cleaned_dirs = []
for name in os.listdir(this_dir):
    found = False
    for f in filters:
        if f in name:
            found = True
    if not found and len(filters) > 0:
        continue

    if os.path.isdir(os.path.join(this_dir, name)):
        run_path = os.path.join(this_dir, name, "run.py")
        if os.path.exists(run_path):
            if clean:
                proc = run_py(f"{__file__} {name} --clean")
                if proc.returncode != 0 or verbose:
                    print(proc.stdout)
                
                cleaned_dirs.append(f"{this_dir}/{name}")
                continue

            print(f"Running {name}... ", end="")
            sys.stdout.flush()
            
            proc = run_py(f"{__file__} {name}")
            if proc.returncode != 0:
                print("\033[0;31mFAILED\033[0m")
            else:
                print("\033[0;32mpass\033[0m")

            if proc.returncode != 0 or verbose:
                print("####         STDOUT/STDERR     ####")
                print(proc.stdout)
                print("####     END STDOUT/STDERR     ####")

            results.append(TestResult(name, proc.returncode == 0))

if clean:
    print(f"Cleaned {len(cleaned_dirs)} directorie(s)")
    if verbose:
        print(cleaned_dirs)
else:
    failed_tests = len([ 1 for r in results if not r.passed ])
    if failed_tests > 0:
        print(f"\033[0;31mFailed {len(results)-failed_tests}/{len(results)} tests\033[0m")
    else:
        print(f"\033[0;32mSuccess {len(results)-failed_tests}/{len(results)} tests\033[0m")