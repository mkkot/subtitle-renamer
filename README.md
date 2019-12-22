# subtitle-renamer
Unzips and renames subtitle files according to movie files. If multiple subtitle files found, tries to find the best one, basing on the name of subtitles file. Also changes every .txt extension into .srt.

This is a preview version which is dedicated to work with Xfce's filemanager Thunar (it collects path to the directory from address bar of an open window). However, you can provide a path as first argument, so you don't need Thunar to use this script. Also, it works only with series. Normal movies are not supported in this version.

If you use Thunar however, change variable thunar_window_name value to something that is used in your language.
Also, I'm using "Mouse cursor activates the window" setting (xfce4-settings/File manager). To get it working with "Mouse click activates the window" you will have to change xdotool command.

Honestly, I don't think this script will be very useful to anyone. In the current form it's not really portable. However, every other script that I found here for this task was doing something wrong. This one does it right. So I shared it. Maybe someone will use this code to learn or to fork this project. Merge Requests improving the situation are welcome.

## Usage

subtitle-renamer.py /path/to/directory/with/series
or
just subtitle-renamer.py if you're using Thunar with "Mouse cursor activates the window".

## Requirements
PTN
pyperclip

xdotool
zenity

### Optional
Thunar
