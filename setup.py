import sys, os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "godaddypy", "configparser", "time", "dns.resolver", "tld"],
    "build_exe": "build"    
}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = "Console"

setup(
    name = "letsencrypt-godaddy",
    version = "1.2",
    description = "letsencrypt-godaddy",
    options = {"build_exe": build_exe_options},
    executables = [Executable("auth.py", base=base), Executable("clean.py", base=base)]
)

print('Compiling Golang...')
try:
    if os.name == 'nt':
        os.system('go build -tags win -o main.exe')
        os.system('move /Y main.exe build')
    else:
        os.system('go build main.go -o main')
        os.system('mv -f main build')
    print('Compile completed!')
except Exception as e:
    sys.exit(f'Compile error: {e}')