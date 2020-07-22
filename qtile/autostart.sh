#!/bin/sh
~/.fehbg &
flameshot &
picom &
mpd &
dunst &
xmodmap ~/.Xmodmap &
xautolock -time 15 -locker 'slock' &
xrdb .Xresources &
~/.screenlayout/fix_monitors_qtile.sh &
