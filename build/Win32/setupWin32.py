# Replace {YOUR PYTHON DIR} with the path of your Python install. If needed change tcl/tk version.
# Replace {YOUR WORKING DIR} with the path of the directory of Isaac Debug Helper files.
# Then run build.bat or manually run "python setupWin32.py build". 

import os
from cx_Freeze import *

os.environ['TCL_LIBRARY'] = '{YOUR PYTHON DIR}/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = '{YOUR PYTHON DIR}/tcl/tk8.6'


buildOptions = dict(
    include_files=['{YOUR PYTHON DIR}/tcl86t.dll', '{YOUR PYTHON DIR}/tk86t.dll', "{YOUR WORKING DIR}/config.cfg", "{YOUR WORKING DIR}/Icon.ico"],
	packages = ["psutil", "tkinter"],
	optimize = "2"
)

executables = [
    Executable(script='main.py', base='Win32GUI', targetName='Isaac Debug Helper.exe', icon='icon.ico')
]

setup(name='Isaac Debug Helper',
      version='2.1.0',
      description='A log reader for The Binding of Isaac',
	  options = dict(build_exe = buildOptions),
      executables=executables
)
