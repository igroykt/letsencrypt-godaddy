import sys, os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "godaddypy", "configparser", "time", "logging", "dns.resolver", "tld"],
    "build_exe": "build"    
}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None

setup(
    name = "letsencrypt-godaddy",
    version = "1.2",
    description = "letsencrypt-godaddy",
    options = {"build_exe": build_exe_options},
    executables = [Executable("auth.py"), Executable("clean.py")]
)

print('Compiling Golang...')
try:
    if os.name != 'nt':
        with open('main.go', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('//syscall', 'syscall').replace('/*out.SysProcAttr = &syscall.SysProcAttr {', 'out.SysProcAttr = &syscall.SysProcAttr {').replace('}*/', '}')
        with open('main.go', 'w') as file:
            file.write(filedata)
    os.system('go build main.go')
    if os.name == 'nt':
        os.rename('main.exe', 'build/main.exe')
    else:
        os.rename('main', 'build/main')
    print('Compile completed!')
except Exception as e:
    sys.exit(f'Compile error: {e}')