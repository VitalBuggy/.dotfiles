# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
colors = [["#272822", "#272822"], #nord0
          ["#272822", "#272822"], #nord1
          ["#75715e", "#75715e"], #nord2
          ["#75715e", "#75715e"], #nord3
          ["#f8f8f2", "#f8f8f2"], #nord4
          ["#f8f8f2", "#f8f8f2"], #nord5
          ["#f9f8f5", "#f9f8f5"], #nord6
          ["#a1efe4", "#a1efe4"], #nord7
          ["#a1efe4", "#a1efe4"], #nord8
          ["#66d9ef", "#66d9ef"], #nord9
          ["#66d9ef", "#66d9ef"], #nord10
          ["#f92672", "#f92672"], #nord11
          ["#f4bf75", "#f4bf75"], #nord12
          ["#f4bf75", "#f4bf75"], #nord13
          ["#a6e22e", "#a6e22e"], #nord14
          ["#ae81ff", "#ae81ff"]] #nord15


from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
import os
import re
import socket
import subprocess
import logging

from typing import List  # noqa: F401

####### MISC FUNCTIONS #######
@lazy.function
def float_to_front(qtile):
    logging.info("bring floating windows to front")
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

####### KEYBINDS #######

mod = "mod1"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),

    # Shrink and grow the window sizes
    Key([mod], "h", lazy.layout.shrink()),
    Key([mod], "l",lazy.layout.grow()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod, "shift"], "Return", lazy.spawn("st")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "c", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "s", lazy.window.toggle_floating()),

    # APPLICATIONS

    Key([mod], "p", lazy.spawn(f"dmenu_run -nb {colors[0][0]} -nf {colors[4][0]} -sb {colors[11][0]} -sf {colors[0][0]}")),
    Key([mod, "shift"], "p", lazy.spawn("rofi -show drun -theme bruh -show-icons")),

    # Volume Controls
    Key([mod], "equal", lazy.spawn("pamixer --allow-boost -i 5")),
    Key([mod, "shift"], "equal", lazy.spawn("pamixer --allow-boost -i 15")),
    Key([mod], "minus", lazy.spawn("pamixer --allow-boost -d 5")),
    Key([mod, "shift"], "minus", lazy.spawn("pamixer --allow-boost -d 15")),

    # Mute Mic
    Key([mod, "control"], "m", lazy.spawn("amixer set Capture toggle")),

    Key([mod], "m", lazy.spawn("st ncmpcpp")),
    Key([mod], "a", lazy.spawn("firefox-bin"))
]

######## COLORS ########

# colors = [["#273136", "#273136"], # panel background
          # ["#434758", "#434758"], # background for current screen tab
          # ["#e1e2e3", "#e1e2e3"], # font color for group names
          # ["#f76c7c", "#f76c7c"], # border line color for current tab
          # ["#1c1e1f", "#1c1e1f"], # border line color for other tab and odd widgets
          # ["#e3d367", "#e3d367"], # color for the even widgets
          # ["#e1e2e3", "#e1e2e3"]] # window name

# colors = [["#272822", "#272822"], #nord0
          # ["#272822", "#272822"], #nord1
          # ["#75715e", "#75715e"], #nord2
          # ["#75715e", "#75715e"], #nord3
          # ["#f8f8f2", "#f8f8f2"], #nord4
          # ["#f8f8f2", "#f8f8f2"], #nord5
          # ["#f9f8f5", "#f9f8f5"], #nord6
          # ["#a1efe4", "#a1efe4"], #nord7
          # ["#a1efe4", "#a1efe4"], #nord8
          # ["#66d9ef", "#66d9ef"], #nord9
          # ["#66d9ef", "#66d9ef"], #nord10
          # ["#f92672", "#f92672"], #nord11
          # ["#f4bf75", "#f4bf75"], #nord12
          # ["#f4bf75", "#f4bf75"], #nord13
          # ["#a6e22e", "#a6e22e"], #nord14
          # ["#ae81ff", "#ae81ff"]] #nord15


######## WORKSPACE NAMES ########

group_names = '一 二 三 四 五 六 七 八 九'.split()
groups = [Group(name, layout='monadtall') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]

layout_theme = {"border_width": 2,
                "margin": 20,
                "border_focus": "f76c7c",
                "border_normal": "273136"
}


layouts = [
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme)

]

####### WIDGETS #######

widget_defaults = dict(
    font='FiraCode',
    fontsize=12,
    padding=0,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def init_widget_list():
    widget_list = [
            widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[6],
                        background = colors[0]
                        ),
               widget.GroupBox(font="Terminus",
                        fontsize = 12,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = colors[6],
                        inactive = colors[6],
                        rounded = False,
                        highlight_color = colors[3],
                        highlight_method = "block",
                        this_current_screen_border = colors[3],
                        this_screen_border = colors [0],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[6],
                        background = colors[0]
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        ),
               widget.WindowName(
                       foreground = colors[14],
                        background = colors[0],
                        padding = 0
                        ),
               widget.TextBox(
                       text=" Vol:",
                        foreground=colors[14],
                        background=colors[0],
                        padding = 0
                        ),
               widget.Volume(
                        foreground = colors[14],
                        background = colors[0],
                        padding = 5
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        ),
               widget.CurrentLayout(
                        foreground = colors[14],
                        background = colors[0],
                        padding = 5
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        ),
               widget.Clock(
                        foreground = colors[14],
                        background = colors[0],
                        format="%A, %B %d  [ %I:%M %p ]"
                        ),
    ]
    return widget_list

##### SCREENS #####

def init_widget_screen1():
    widgets_screen1 = init_widget_list()
    return widgets_screen1

def init_widget_screen2():
    widgets_screen2 = init_widget_list()
    return widgets_screen2

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widget_screen1(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widget_screen1(), opacity=0.95, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widget_list()
    widgets_screen1 = init_widget_screen1()
    widgets_screen2 = init_widget_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"


######## AUTOSTART ######## 
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])


# Steam specific floating settings
@hook.subscribe.client_new
def float_steam(window):
    wm_class = window.window.get_wm_class()
    w_name = window.window.get_name()
    if (
        wm_class == ("Steam", "Steam")
        and (
            w_name != "Steam"
            # w_name == "Friends List"
            # or w_name == "Screenshot Uploader"
            # or w_name.startswith("Steam - News")
            or "PMaxSize" in window.window.get_wm_normal_hints().get("flags", ())
        )
    ):
        window.floating = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
