# Isaac Debug Helper

This tool is a fork of [Isaac Modding Helper Tool] by Dogeek, and is aimed at anyone who wishes to create mods for *The Binding of Isaac*. It's a log reader: reads the log files directly and displays the content in a user-friendly graphical user interface. 
The goal of Dogeek's project is to create a complete software suite for modding of *The Binding of Isaac*.

[License]: GNU GPL 3.0

## Requirements :

 - Python 3.x (tested on 3.6.4 on Windows)
 
### Optional

 - [psutil] (pip install psutil) - Needed for autoreload feature.

 All other libraries are standard libraries.

# Features :

 - *Start* and *Stop* menu buttons, to load or reload the script when debugging
 - Color highlighting errors, warnings, informations and debug information
 - A GUI designed for ease of use, with most of the window dedicated to the output
 - The log file is automatically found, no need for any configuration, it works out of the box
 - Fully designed to be cross-platform (at least as long as Python support it)
 - Dynamic LUA memory usage while the debugger is running, with a progress bar to make the logs even more readable
 - Scrollbar for the text widget
 - Option Toolbox to set up custom tags and filters for the debugger, changing colors etc
 - Auto reload feature if *The Binding of Isaac* is restarted
 - Store preferences in a local config file
 - Slider for maximum LUA memory (from 1KB to 10KB) in the options
 - About menu

# Changelog
See [CHANGELOG.md]
# About the project :

A modification by [Team Dodo] of [Isaac Modding Helper Tool]. Original project's credits:
 - Lead Developer: Dogeek
 - Debugger Idea: Krayz
 - Layout Design: Dogeek

[CHANGELOG.md]: /CHANGELOG.md
[Isaac Modding Helper Tool]: https://github.com/Dogeek/isaac-debug-helper
[License]: https://github.com/Dogeek/isaac-debug-helper/issues/2
[psutil]: https://github.com/giampaolo/psutil
[Team Dodo]: https://github.com/teamdodo/
