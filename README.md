# Isaac debug helper - Fork
Fork of https://github.com/Dogeek/isaac-debug-helper

# Requirements :
 - Python 3.x (tested on 3.6.4 on windows)
 
OPTIONAL

 - psutil (pip install psutil) - https://github.com/giampaolo/psutil
 
# Known issues 
* Options window is named "Isaac debug helper" instead of "Options" in spite of attempts of giving it the correct name.
* Lua memory usage counter does NOT have transparent background, then covers part of the progress bar. It's a Tkinter issue: labels can't have transparent background.
* When opening color picker, options window goes on the background of main window

# Changelog (differences from original Isaac debug helper)
# GUI
+ Added debugger status indicator
+ Added Lua memory usage counter on the progress bar.
+ Added Clear text function
+ Reset do defaults option and adjusted buttons size

# DEBUG
* Fixed "SyntaxError: encoding problem: utf8" when launching by shell or double-click

Changed encoding name to utf-8 in .py files.

* Fixed options not saving, fixed options not opening again if closed

It looked like a problem with global variable: solved merging options.py and main.py. Brutal solution but it works.


# CHANGES AND IMPROVEMENTS
* Options

Added function called on WM_DELETE_WINDOW of Options window.

Options are now saved in config.cfg both when onOkButton and on_closing are triggered.

Options not saved when option window is open and user changes option then closes parent window. In this case user is supposed to discard changes.

* Removed old #TODO
* Added version in About
* Handle config.cfg not found or damaged (TODO: improve code of this feature)
* Handle psutil not found
* Handle case of click on "Stop" when debugger has never been started. Otherwise raises exception "DebugFrame has no object log_f".
* Add Team Dodo credits
