# Replace {YOUR WORKING DIR} with the path of the directory of Isaac Debug Helper files.
# Then run build.sh or manually run "python3 setupLinux.py build". 

from cx_Freeze import *

buildOptions = dict(
    include_files=["{YOUR WORKING DIR}/config.cfg"],
    optimize = "2",
    packages = ["psutil", "tkinter"]
)

executables = [
    Executable('main.py', base=None, icon="Icon.png", targetName="Isaac Debug Helper")
]

setup(name='Isaac Debug Helper',
    version='2.1.0',
    description='A log reader for The Binding of Isaac',
    options = dict(build_exe = buildOptions),
    executables=executables
)
