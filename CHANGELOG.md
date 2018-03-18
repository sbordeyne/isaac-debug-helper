# Changelog
All notable changes to *Isaac Debug Helper* project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
None

## 2.1.0 - 2018-02-26

### Added 
- Check for updates (check if a new version is available for download).
- Exceptions are now reported as errors.

## 2.0.0 - 2018-02-11

### Added 
- GUI: debugger status indicator.
- GUI: Lua memory usage counter on the progress bar.
- *Clear* text function.
- Button to reset options to default.
- Version number and Team Dodo credits in *About*.
- Handle config.cfg not found or damaged.
- Handle psutil not found.

### Changed
- Added function called on WM_DELETE_WINDOW of Options window.
- Options are now saved in config.cfg both when *Ok* button is clicked and when Isaac debug helper is closedonOkButton and on_closing are triggered.
- Options are **not** saved when *Options* window is open, user changes settings then closes parent window. In this case user is supposed to discard changes.
### Removed
- Old #TODOs in code

### Fixed
- GUI: adjusted buttons size in Options.
- "SyntaxError: encoding problem: utf8" when launching by shell or double-click.
	* Changed encoding name to utf-8 in .py files.
- Options not saving, Options not opening again after being closed.
	* It looked like a problem with global variables: solved merging options.py and main.py. Brutal solution but it works.
- "DebugFrame has no object log_f" when clicking on *Stop* but the debugger has never been started before.
	
## Prior to fork - up to 2018-02-11
See [Isaac Modding Helper Tool] by Dogeek

[Isaac Modding Helper Tool]: https://github.com/Dogeek/isaac-debug-helper/
