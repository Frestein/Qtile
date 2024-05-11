# Keys
from libqtile.config import EzKey as Key, EzKeyChord as KeyChord
from libqtile.lazy import lazy

# Mouse
from libqtile.config import EzClick as Click, EzDrag as Drag

# Groups
from libqtile.config import Group, Match

# Layouts
from libqtile import layout

# Screens
from libqtile.config import Screen
from libqtile import bar, widget

# ScratchPad and DropDown
# from libqtile.config import ScratchPad, DropDown

from os import path, environ
from subprocess import Popen
from libqtile import hook, qtile


# Environments ------------------------------

# Scripts/Apps variables
home = path.expanduser("~")
autostart_sh = home + "/.config/qtile/scripts/qtile_autostart"
color_picker = home + "/.config/qtile/scripts/qtile_colorpicker"
polybar = home + "/.config/qtile/scripts/qtile_bar"
volume = home + "/.config/qtile/scripts/qtile_volume"
screenshot = home + "/.config/qtile/scripts/qtile_screenshot"
file_manager = "nemo"
web_browser = "firefox"
terminal = "kitty --session=session.conf"
discord = "vesktop"
telegram = "telegram-desktop"
music_player = "muffon"
password_manager = "keepassxc"
rofi_applets = home + "/.config/qtile/scripts/"
notify_cmd = "dunstify -u low -h string:x-dunst-stack-tag:qtileconfig"

# System environments -----------------------
environ["KITTY_CONFIG_DIRECTORY"] = home + "/.config/qtile/kitty"


# Startup ----------------------------------
@hook.subscribe.startup_once
def autostart():
    Popen([autostart_sh])


# Key Bindings ------------------------------

modifier_keys = {
    "M": "mod4",
    "A": "mod1",
    "S": "shift",
    "C": "control",
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Terminal --
    Key("M-<Return>", lazy.spawn(terminal), desc="Launch terminal"),
    # GUI Apps --
    Key("M-w", lazy.spawn(web_browser), desc="Launch web browser"),
    Key("M-m", lazy.spawn(music_player), desc="Launch music player"),
    Key("M-k", lazy.spawn(password_manager), desc="Launch password manager"),
    Key("M-t", lazy.spawn(telegram), desc="Launch telegram"),
    Key("M-d", lazy.spawn(discord), desc="Launch discord"),
    Key("M-S-f", lazy.spawn(file_manager), desc="Launch file manager"),
    # Rofi Applets --
    Key("A-<F1>", lazy.spawn(rofi_applets + "rofi_launcher"), desc="Run application launcher"),
    Key("A-<F2>", lazy.spawn(rofi_applets + "rofi_runner"), desc="Run command runner"),
    Key("M-n", lazy.spawn(rofi_applets + "network_menu"), desc="Run network manager applet"),
    Key("M-x", lazy.spawn(rofi_applets + "rofi_powermenu"), desc="Run powermenu applet"),
    Key("M-r", lazy.spawn(rofi_applets + "rofi_asroot"), desc="Run asroot applet"),
    Key("M-s", lazy.spawn(rofi_applets + "rofi_screenshot"), desc="Run screenshot applet"),
    # Function keys : Volume --
    Key("<XF86AudioRaiseVolume>", lazy.spawn(volume + " --inc"), desc="Raise speaker volume"),
    Key("<XF86AudioLowerVolume>", lazy.spawn(volume + " --dec"), desc="Lower speaker volume"),
    Key("<XF86AudioMute>", lazy.spawn(volume + " --toggle"), desc="Toggle mute"),
    Key("<XF86AudioMicMute>", lazy.spawn(volume + " --toggle-mic"), desc="Toggle mute for mic"),
    # Function keys : Media --
    Key("<XF86AudioNext>", lazy.spawn("playerctl next"), desc="Next track"),
    Key("<XF86AudioPrev>", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key("<XF86AudioPlay>", lazy.spawn("playerctl play-pause"), desc="Toggle play/pause"),
    Key("<XF86AudioStop>", lazy.spawn("playerctl stop"), desc="Stop playing"),
    # Screenshots --
    Key("<Print>", lazy.spawn(screenshot + " --now"), desc="Take Screenshot"),
    Key("C-<Print>", lazy.spawn(screenshot + " --in5"), desc="Take Screenshot in 5 seconds"),
    Key("S-<Print>", lazy.spawn(screenshot + " --in10"), desc="Take Screenshot in 10 seconds"),
    Key("C-S-<Print>", lazy.spawn(screenshot + " --win"), desc="Take Screenshot of active window"),
    Key("M-<Print>", lazy.spawn(screenshot + " --area"), desc="Take Screenshot of selected area"),
    # Misc --
    Key("M-p", lazy.spawn(color_picker), desc="Run colorpicker"),
    Key("A-C-l", lazy.spawn("betterlockscreen --lock --time-format %H:%M"), desc="Run lockscreen"),
    # WM Specific --
    Key("M-c", lazy.window.kill(), desc="Kill focused window"),
    # Control Qtile
    Key("M-C-r", lazy.reload_config(), lazy.spawn(notify_cmd + ' "Configuration Reloaded!"'), desc="Reload the config"),
    Key("M-C-s", lazy.restart(), lazy.spawn(notify_cmd + ' "Restarting Qtile..."'), desc="Restart Qtile"),
    Key("M-C-q", lazy.shutdown(), lazy.spawn(notify_cmd + ' "Exiting Qtile..."'), desc="Shutdown Qtile"),
    # Switch between windows
    Key("M-<Left>", lazy.layout.left(), desc="Move focus to left"),
    Key("M-<Right>", lazy.layout.right(), desc="Move focus to right"),
    Key("M-<Down>", lazy.layout.down(), desc="Move focus down"),
    Key("M-<Up>", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-S-<Left>", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key("M-S-<Right>", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key("M-S-<Down>", lazy.layout.shuffle_down(), desc="Move window down"),
    Key("M-S-<Up>", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-C-<Left>", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key("M-C-<Right>", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key("M-C-<Down>", lazy.layout.grow_down(), desc="Grow window down"),
    Key("M-C-<Up>", lazy.layout.grow_up(), desc="Grow window up"),
    Key("M-C-<Return>", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle floating and fullscreen
    Key("M-z", lazy.window.toggle_floating(), desc="Put the focused window to/from floating mode"),
    Key("M-f", lazy.window.toggle_fullscreen(), desc="Put the focused window to/from fullscreen mode"),
    # Go to next/prev group
    Key("M-A-<Right>", lazy.screen.next_group(), desc="Move to the group on the right"),
    Key("M-A-<Left>", lazy.screen.prev_group(), desc="Move to the group on the left"),
    # Back-n-forth groups
    Key("M-b", lazy.screen.toggle_group(), desc="Move to the last visited group"),
    # Change focus to other window
    Key("M-<Tab>", lazy.layout.next(), desc="Move window focus to other window"),
    # Toggle between different layouts as defined below
    Key("M-S-<space>", lazy.next_layout(), desc="Toggle between layouts"),
    # Increase the space for master window at the expense of slave windows
    Key("M-<equal>", lazy.layout.increase_ratio(), desc="Increase the space for master window"),
    # Decrease the space for master window in the advantage of slave windows
    Key("M-<minus>", lazy.layout.decrease_ratio(), desc="Decrease the space for master window"),
    # Toggle between split and unsplit sides of stack.
    Key("M-S-s", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    # Modes: Reize
    KeyChord(
        "M-S-r",
        [
            Key("<Left>", lazy.layout.grow_left()),
            Key("<Right>", lazy.layout.grow_right()),
            Key("<Down>", lazy.layout.grow_down()),
            Key("<Up>", lazy.layout.grow_up()),
        ],
        mode=True,
        name="Resize",
    ),
    # Modes: Layouts
    KeyChord(
        "M-S-l",
        [
            Key("<Left>", lazy.prev_layout()),
            Key("<Right>", lazy.next_layout())
        ],
        mode=True,
        name="Layouts",
    ),
]

# Mouse Bindings ------------------------------

# Drag floating layouts.
mouse = [
    Drag("M-1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag("M-3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click("M-2", lazy.window.bring_to_front()),
]

# Groups -------------------------------------


# Auto-switching group when a new window is launched
@hook.subscribe.client_managed
def auto_switch(window):
    if window.group.name != qtile.current_group.name:
        window.group.cmd_toscreen()


groups = [
    Group("1", matches=[Match(wm_class="kitty")]),
    Group(
        "2",
        matches=[
            Match(wm_class="jetbrains-studio"),
            Match(wm_class="jetbrains-pycharm"),
            Match(wm_class="jetbrains-toolbox"),
        ],
    ),
    Group(
        "3",
        matches=[
            Match(wm_class="firefox"),
        ],
    ),
    Group(
        "4",
        matches=[
            Match(wm_class="Nemo"),
            Match(wm_class="thunderbird"),
        ],
    ),
    Group(
        "5",
        matches=[
            Match(wm_class="obsidian"),
            Match(wm_class="Zathura"),
        ],
    ),
    Group(
        "6",
        matches=[
            Match(wm_class="TelegramDesktop"),
            Match(wm_class="vesktop"),
        ],
    ),
    Group(
        "7",
        matches=[
            Match(wm_class="steam"),
            Match(wm_class="muffon"),
        ],
    ),
    Group(
        "8",
        matches=[
            Match(wm_class="jamesdsp"),
            Match(wm_class="KeePassXC"),
        ],
    ),
]

for i in groups:
    keys.extend(
        [
            # mod + number of group = switch to group
            Key(
                "M-" + i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + number of group = switch to & move focused window to group
            Key(
                "M-S-" + i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# Layouts -----------------------------------
var_bg_color = "#2e3440"
var_active_bg_color = "#81A1C1"
var_active_fg_color = "#2e3440"
var_inactive_bg_color = "#3d4555"
var_inactive_fg_color = "#D8DEE9"
var_urgent_bg_color = "#BF616A"
var_urgent_fg_color = "#D8DEE9"
var_section_fg_color = "#EBCB8B"
var_active_color = "#81A1C1"
var_normal_color = "#3d4555"
var_border_width = 2
var_margin = [5, 5, 5, 5]
var_gap_top = 45
var_gap_bottom = 5
var_gap_left = 5
var_gap_right = 5
var_font_name = "JetBrains Mono"

layouts = [
    # Extension of the Stack layout
    layout.Columns(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        fair=False,
        grow_amount=10,
        insert_position=0,
        margin=var_margin,
        margin_on_single=None,
        num_columns=2,
        split=True,
        wrap_focus_columns=True,
        wrap_focus_rows=True,
        wrap_focus_stacks=True,
    ),
    # Layout inspired by bspwm
    layout.Bsp(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        fair=True,
        grow_amount=10,
        lower_right=True,
        margin=var_margin,
        margin_on_single=None,
        ratio=1.6,
        wrap_clients=False,
    ),
    # This layout divides the screen into a matrix of equally sized cells and places one window in each cell.
    layout.Matrix(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        columns=2,
        margin=var_margin,
    ),
    # Maximized layout
    layout.Max(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        margin=0,
    ),
    # Emulate the behavior of XMonad's default tiling scheme.
    layout.MonadTall(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="after_current",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Emulate the behavior of XMonad's ThreeColumns layout.
    layout.MonadThreeCol(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        main_centered=True,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="top",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Emulate the behavior of XMonad's horizontal tiling scheme.
    layout.MonadWide(
        align=0,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        change_ratio=0.05,
        change_size=20,
        margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
        min_secondary_size=85,
        new_client_position="after_current",
        ratio=0.5,
        single_border_width=None,
        single_margin=None,
    ),
    # Tries to tile all windows in the width/height ratio passed in
    layout.RatioTile(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fancy=False,
        margin=var_margin,
        ratio=1.618,
        ratio_increment=0.1,
    ),
    # This layout cuts piece of screen_rect and places a single window on that piece, and delegates other window placement to other layout
    layout.Slice(match=None, side="left", width=256),
    # A mathematical layout, Renders windows in a spiral form by splitting the screen based on a selected ratio.
    layout.Spiral(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        clockwise=True,
        main_pane="left",
        main_pane_ratio=None,
        margin=0,
        new_client_position="top",
        ratio=0.6180469715698392,
        ratio_increment=0.1,
    ),
    # A layout composed of stacks of windows
    layout.Stack(
        autosplit=False,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fair=False,
        margin=var_margin,
        num_stacks=2,
    ),
    # A layout with two stacks of windows dividing the screen
    layout.Tile(
        add_after_last=False,
        add_on_top=True,
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_on_single=False,
        border_width=var_border_width,
        expand=True,
        margin=var_margin,
        margin_on_single=None,
        master_length=1,
        master_match=None,
        max_ratio=0.85,
        min_ratio=0.15,
        ratio=0.618,
        ratio_increment=0.05,
        shift_windows=False,
    ),
    # This layout works just like Max but displays tree of the windows at the left border of the screen_rect, which allows you to overview all opened windows.
    layout.TreeTab(
        active_bg=var_active_bg_color,
        active_fg=var_active_fg_color,
        bg_color=var_bg_color,
        border_width=var_border_width,
        font=var_font_name,
        fontshadow=None,
        fontsize=14,
        inactive_bg=var_inactive_bg_color,
        inactive_fg=var_inactive_fg_color,
        level_shift=0,
        margin_left=0,
        margin_y=0,
        padding_left=10,
        padding_x=10,
        padding_y=10,
        panel_width=200,
        place_right=False,
        previous_on_rm=False,
        section_bottom=0,
        section_fg=var_section_fg_color,
        section_fontsize=14,
        section_left=10,
        section_padding=10,
        section_top=10,
        sections=["Default"],
        urgent_bg=var_urgent_bg_color,
        urgent_fg=var_urgent_fg_color,
        vspace=5,
    ),
    # Tiling layout that works nice on vertically mounted monitors
    layout.VerticalTile(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        margin=var_margin,
    ),
    # A layout with single active windows, and few other previews at the right
    layout.Zoomy(
        columnwidth=300,
        margin=var_margin,
        property_big="1.0",
        property_name="ZOOM",
        property_small="0.1",
    ),
    # Floating layout, which does nothing with windows but handles focus order
    layout.Floating(
        border_focus=var_active_color,
        border_normal=var_normal_color,
        border_width=var_border_width,
        fullscreen_border_width=0,
        max_border_width=0,
    ),
]

# Screens ----------------------------------

# Default Qtile Bar (commented)
"""
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                #widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%I:%M %p"),
                widget.QuickExit(),
            ],
            34,
            background=["000000", "101010"],
            margin=[0,0,0,0],
            opacity=1.0,
            border_width=[2, 0, 0, 0],
            border_color=["303030", "000000", "000000", "000000"]
        ),
    ),
]
"""

# Any third-party statusbar (polybar) with Gaps
screens = [
    Screen(
        right=bar.Gap(var_gap_right),
        left=bar.Gap(var_gap_left),
        bottom=bar.Gap(var_gap_bottom),
        top=bar.Gap(var_gap_top),
    )
]

# General Configuration Variables ------------------------------

# If a window requests to be fullscreen, it is automatically fullscreened.
# Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = True

# When clicked, should the window be brought to the front or not.
# If this is set to "floating_only", only floating windows will get affected (This sets the X Stack Mode to Above.)
bring_front_click = False

# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window.
# When switching focus between screens, If there are no windows in the screen, the cursor will warp to the center of the screen.
cursor_warp = False

# A function which generates group binding hotkeys. It takes a single argument, the DGroups object, and can use that to set up dynamic key bindings.
# A sample implementation is available in 'libqtile/dgroups.py' called `simple_key_binder()`, which will bind groups to "mod+shift+0-10" by default.
dgroups_key_binder = None

# A list of Rule objects which can send windows to various groups based on matching criteria.
dgroups_app_rules = []  # type: list

# The default floating layout to use. This allows you to set custom floating rules among other things if you wish.
floating_layout = layout.Floating(
    border_focus=var_active_color,
    border_normal=var_normal_color,
    border_width=var_border_width,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="alacritty-float|Music"),
        Match(wm_class="Lxappearance|Nitrogen"),
        Match(wm_class="Pavucontrol|Xfce4-power-manager-settings|Nm-connection-editor"),
        Match(wm_class="feh|Viewnior|Gpicview|Gimp|MPlayer|Vlc|Spotify"),
        Match(wm_class="Kvantum Manager|qt5ct"),
        Match(wm_class="VirtualBox Manager|qemu|Qemu-system-x86_64"),
        Match(title="branchdialog"),
    ],
)

# Behavior of the _NET_ACTIVATE_WINDOW message sent by applications
#
# urgent: urgent flag is set for the window
# focus: automatically focus the window
# smart: automatically focus if the window is in the current group
# never: never automatically focus any window that requests it
focus_on_window_activation = "smart"

# Controls whether or not focus follows the mouse around as it moves across windows in a layout.
follow_mouse_focus = True

# Default settings for bar widgets.
widget_defaults = dict(
    font=var_font_name,
    fontsize=14,
    padding=5,
)

# Same as `widget_defaults`, Default settings for extensions.
extension_defaults = widget_defaults.copy()

# Controls whether or not to automatically reconfigure screens when there are changes in randr output configuration.
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
