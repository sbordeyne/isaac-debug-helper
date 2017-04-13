# Isaac Modding Helper Tool

This tool is aimed at anyone who wishes to mod The Binding of Isaac. It reads the log files directly and displays the content in a user-friendly graphical user interface. Currently, there are not many features, but more is planned, to make this a complete software suite for modding Isaac.

All the code in this repository is under the Creative Commons License. You can use and modify it however you want, as long as you give credit where credit is due.

# Features :

 - Start and Stop menu buttons, to load or reload the script when debugging
 - Color highlighting errors, warnings, informations and debug information
 - A GUI designed for ease of use, with most of the window dedicated to the output
 - The log file is automatically found, no need for any configuration, it works out of the box
 - Fully designed to be cross-platform (at least as long as Python support it)
 
# Planned Features :

 - A pixel art tool specifically for isaac, with integrated palettes, image format, and file saving straight into your mod's' folder
 - Option Toolbox to set up custom tags and filters for the debugger, changing colors etc
 - Dynamic LUA memory usage while the debugger is running, with a progress bar to make the logs even more readable
 - Additional infos that usually clutter the text available in another tab, with disablable labels and widgets to display the currenly played music for instance
 - About menu
 - Options Menu (to trigger the option toolbox)
 - Add a scrollbar to the text widget
 - Auto reload feature if isaac is restarted
 - Enhanced bug reporter that'll create automatic issues on github for specific mods

# About the project :

I do that on my free time, I'll try to make all those planned features as soon as possible.

 -- Lead Developer : Dogeek
 -- Debugger Idea : Krayz
 -- Layout Design : Dogeek

This started as a need, so that's why the current build is not very polished. All you need to run this script is Python 3.6, as everything has been coded with standard libraries (tkinter ; os ; sys ; time). You can also download a prebuilt version straight off of github. This software is completely portable as well, you can put it on a USB stick as its "compiled" version and it'll work just fine.
