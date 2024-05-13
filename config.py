# vim:fileencoding=utf-8:foldmethod=marker
from libqtile.config import EzKey as Key, EzKeyChord as KeyChord
from libqtile.config import EzClick as Click, EzDrag as Drag
from libqtile.config import Group, Match, Screen
from libqtile.lazy import lazy
from libqtile import qtile, bar, widget, layout, hook
from os import path, environ
from subprocess import Popen

# App/Script Variables {{{

home = path.expanduser("~")
autostart_sh = home + "/.config/qtile/scripts/qtile_autostart"
color_picker = home + "/.config/qtile/scripts/qtile_colorpicker"
polybar = home + "/.config/qtile/scripts/qtile_bar"
volume = home + "/.config/qtile/scripts/qtile_volume"
screenshot = home + "/.config/qtile/scripts/qtile_screenshot"
file_manager = "nemo"
web_browser = "firefox"
terminal = "kitty --session=session.conf"
android_studio = home + "/.config/qtile/scripts/studio.sh"
discord = "webcord"
telegram = "telegram-desktop"
music_player = "muffon"
password_manager = "keepassxc"
rofi_applets = home + "/.config/qtile/scripts/"
notify_cmd = "dunstify -u low -h string:x-dunst-stack-tag:qtileconfig"

# }}}
# Environments {{{

environ["KITTY_CONFIG_DIRECTORY"] = home + "/.config/qtile/kitty"

# }}}
# Autostart {{{

@hook.subscribe.startup_once
def autostart():
    Popen([autostart_sh])

# }}}
# Key Bindings {{{

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
    Key("M-a", lazy.spawn(android_studio), desc="Launch Android Studio"),
    Key("M-w", lazy.spawn(web_browser), desc="Launch web browser"),
    Key("M-m", lazy.spawn(music_player), desc="Launch music player"),
    Key("M-k", lazy.spawn(password_manager), desc="Launch password manager"),
    Key("M-t", lazy.spawn(telegram), desc="Launch telegram"),
    Key("M-d", lazy.spawn(discord), desc="Launch discord"),
    Key("M-S-f", lazy.spawn(file_manager), desc="Launch file manager"),
    # Rofi Applets --
    Key("A-<F1>", lazy.spawn(rofi_applets + "rofi_launcher"), desc="Run application launcher"),
    Key("M-r", lazy.spawn(rofi_applets + "rofi_runner"), desc="Run command runner"),
    Key("M-n", lazy.spawn(rofi_applets + "network_menu"), desc="Run network manager applet"),
    Key("M-x", lazy.spawn(rofi_applets + "rofi_powermenu"), desc="Run powermenu applet"),
    Key("A-r", lazy.spawn(rofi_applets + "rofi_asroot"), desc="Run asroot applet"),
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
# }}}
# Mouse Key Bindings {{{

# Drag floating layouts.
mouse = [
    Drag("M-1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag("M-3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click("M-2", lazy.window.bring_to_front()),
]

# }}}
# Groups {{{

# Auto-switching group when a new window is launched
@hook.subscribe.client_managed
def auto_switch(window):
    if window.group.name != qtile.current_group.name:
        window.group.cmd_toscreen()


groups = [
    Group(
        name="1",
        matches=[
            Match(wm_class="kitty"),
        ],
        label="",
    ),
    Group(
        name="2",
        matches=[
            Match(wm_class="jetbrains-studio"),
            Match(wm_class="jetbrains-pycharm"),
            Match(wm_class="jetbrains-toolbox", title="JetBrains Toolbox"),
        ],
        label="",
    ),
    Group(
        name="3",
        matches=[
            Match(wm_class="firefox"),
        ],
        label="󰈹",
    ),
    Group(
        name="4",
        matches=[
            Match(wm_class="Nemo"),
            Match(wm_class="thunderbird"),
        ],
        label="",
    ),
    Group(
        name="5",
        matches=[
            Match(wm_class="obsidian"),
            Match(wm_class="Zathura"),
        ],
        label="",
    ),
    Group(
        name="6",
        matches=[
            Match(wm_class="TelegramDesktop"),
            Match(wm_class="webcord"),
        ],
        label="",
    ),
    Group(
        name="7",
        matches=[
            Match(wm_class="muffon"),
        ],
        label="󰝚",
    ),
    Group(
        name="8",
        matches=[
            Match(wm_class="jamesdsp"),
            Match(wm_class="KeePassXC"),
        ],
        label="",
    ),
    Group(
        name="9",
        matches=[
            Match(wm_class="steam"),
            Match(wm_class="yad_v13_0"),
        ],
        label="",
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
# }}}
# Layout/Widget Variables {{{

border_width = 2
margin = [5, 10, 10, 10]
gap=[45, 5, 5, 5]
font_name = "JetBrains Mono Nerd Font Mono"

colors = [
    ["#32363D", "#32363D"],  # 0
    ["#BF616A", "#BF616A"],  # 1
    ["#A3BE8C", "#A3BE8C"],  # 2
    ["#EBCB8B", "#EBCB8B"],  # 3
    ["#81A1C1", "#81A1C1"],  # 4
    ["#B48EAD", "#B48EAD"],  # 5
    ["#88C0D0", "#88C0D0"],  # 6
    ["#E5E9F0", "#E5E9F0"],  # 7
    ["#4C566A", "#4C566A"],  # 8
    ["#BF616A", "#BF616A"],  # 9
    ["#A3BE8C", "#A3BE8C"],  # 10
    ["#EBCB8B", "#EBCB8B"],  # 11
    ["#81A1C1", "#81A1C1"],  # 12
    ["#B48EAD", "#B48EAD"],  # 13
    ["#8FBCBB", "#8FBCBB"],  # 14
    ["#ECEFF4", "#ECEFF4"],  # 15
    ["#A8AFBC", "#A8AFBC"],  # 16 Inactive tab foreground
    ["#343A46", "#343A46"],  # 17 Inactive tab background
    ["#343A46", "#343A46"],  # 18 GroupBox background
    ["#D8DEE9", "#D8DEE9"],  # 19 Foreground
    ["#2E3440", "#2E3440"],  # 20 Background
    ["#2E3440", "#2E3440"],  # 21 Selection foreground
    ["#D8DEE9", "#D8DEE9"],  # 22 Selection background
]
#}}}
# Layouts {{{

layouts = [
    # Extension of the Stack layout
    layout.Columns(
        border_focus=colors[4],
        border_normal=colors[20],
        border_on_single=False,
        border_width=border_width,
        fair=False,
        grow_amount=10,
        insert_position=0,
        margin=margin,
        margin_on_single=None,
        num_columns=2,
        split=True,
        wrap_focus_columns=True,
        wrap_focus_rows=True,
        wrap_focus_stacks=True,
    ),
    # Layout inspired by bspwm
    layout.Bsp(
        border_focus=colors[4],
        border_normal=colors[20],
        border_on_single=False,
        border_width=border_width,
        fair=True,
        grow_amount=10,
        lower_right=True,
        margin=margin,
        margin_on_single=None,
        ratio=1.6,
        wrap_clients=False,
    ),
    # This layout divides the screen into a matrix of equally sized cells and places one window in each cell.
    layout.Matrix(
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        columns=2,
        margin=margin,
    ),
    # Maximized layout
    layout.Max(
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        margin=0,
    ),
    # Emulate the behavior of XMonad's default tiling scheme.
    layout.MonadTall(
        align=0,
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
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
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
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
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
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
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        fancy=False,
        margin=margin,
        ratio=1.618,
        ratio_increment=0.1,
    ),
    # This layout cuts piece of screen_rect and places a single window on that piece, and delegates other window placement to other layout
    layout.Slice(match=None, side="left", width=256),
    # A mathematical layout, Renders windows in a spiral form by splitting the screen based on a selected ratio.
    layout.Spiral(
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
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
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        fair=False,
        margin=margin,
        num_stacks=2,
    ),
    # A layout with two stacks of windows dividing the screen
    layout.Tile(
        add_after_last=False,
        add_on_top=True,
        border_focus=colors[4],
        border_normal=colors[20],
        border_on_single=False,
        border_width=border_width,
        expand=True,
        margin=margin,
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
        active_bg=colors[4],
        active_fg=colors[20],
        bg_color=colors[20],
        border_width=border_width,
        font=font_name,
        fontshadow=None,
        fontsize=14,
        inactive_bg=colors[20],
        inactive_fg=colors[19],
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
        section_fg=colors[3],
        section_fontsize=14,
        section_left=10,
        section_padding=10,
        section_top=10,
        sections=["Default"],
        urgent_bg=colors[20],
        urgent_fg=colors[19],
        vspace=5,
    ),
    # Tiling layout that works nice on vertically mounted monitors
    layout.VerticalTile(
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        margin=margin,
    ),
    # A layout with single active windows, and few other previews at the right
    layout.Zoomy(
        columnwidth=300,
        margin=margin,
        property_big="1.0",
        property_name="ZOOM",
        property_small="0.1",
    ),
    # Floating layout, which does nothing with windows but handles focus order
    layout.Floating(
        border_focus=colors[4],
        border_normal=colors[20],
        border_width=border_width,
        fullscreen_border_width=0,
        max_border_width=0,
    ),
]
# }}}
# Widgets {{{


class CustomClock(widget.Clock):
    def __init__(self, **config):
        widget.Clock.__init__(self, **config)
        self.add_callbacks({"Button1": self.toggle_format})
        self.format_options = ["%I:%M", "%Y/%m/%d"]
        self.current_format_index = 0
        self.update_interval = 0.1

    def toggle_format(self):
        self.current_format_index = (self.current_format_index + 1) % len(
            self.format_options
        )
        self.format = self.format_options[self.current_format_index]

# Default settings for bar widgets.
widget_defaults = dict(
    font=font_name,
    fontsize=14,
    padding=10,
    background=colors[20],
    foreground=colors[20],
)

current_layout_icon = widget.CurrentLayoutIcon(
    scale=0.5,
    background=colors[4],
)
group_box = widget.GroupBox(
    fontsize=20,
    borderwidth=0,
    disable_drag=True,
    active=colors[7],
    inactive=colors[7],
    hide_unused=True,
    highlight_method="block",
    highlight_color=colors[1],
    this_current_screen_border=colors[4],
    this_screen_border=colors[20],
    urgent_alert_method="line",
    urgent_border=colors[5],
    urgent_text=colors[7],
    use_mouse_wheel=True,
)
windowname_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[4],
)
windowname = widget.WindowName(
    foreground=colors[4],
)
volume_icon = widget.TextBox(
    text="󰕾",
    fontsize=20,
    background=colors[3],
)
volume = widget.Volume(
    mouse_callbacks={
        "Button1": lazy.spawn(volume + " --inc"),
        "Button3": lazy.spawn(volume + " --dec"),
    },
    get_volume_command="pactl get-sink-volume alsa_output.pci-0000_00_1f.3.analog-stereo ",
    foreground=colors[3],
)
memory_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[2],
)
memory = widget.Memory(
    format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
    measure_mem="G",
    foreground=colors[2],
)
net_icon = widget.TextBox(
    text="󰑩",
    fontsize=20,
    background=colors[6],
)
net = widget.Net(
    interface="enp0s31f6",
    format="{down:.0f} {down_suffix:<0}/{up:.0f} {up_suffix:<0}",
    update_interval=3,
    use_bits=True,
    foreground=colors[6],
)
cpu_icon = widget.TextBox(
    text="󰍛",
    fontsize=20,
    background=colors[4],
)
cpu = widget.CPU(
    format="{load_percent:.0f}%",
    update_interval=3,
    foreground=colors[4],
)
tray_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[5],
)
tray = widget.Systray(
    padding=5,
    icon_size=18,
)
clock_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[1],
)
clock = CustomClock(
    foreground=colors[1],
)

# }}}
# Extensions {{{

# Same as `widget_defaults`, Default settings for extensions.
extension_defaults = widget_defaults.copy()

# }}}
# Screens {{{

screens = [
    Screen(
        top=bar.Bar(
            [
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                current_layout_icon,
                group_box,
                windowname_icon,
                windowname,
                volume_icon,
                volume,
                memory_icon,
                memory,
                net_icon,
                net,
                cpu_icon,
                cpu,
                tray_icon,
                tray,
                widget.Spacer(length=5),
                clock_icon,
                clock,
            ],
            size=28,
            background=["#2d333f", "#2d333f"],
            margin=[10, 10, 5, 10],
            opacity=1,
        ),
    )
]

# }}}
# General Configuration Variables {{{

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
    border_focus=colors[4],
    border_normal=colors[20],
    border_width=border_width,
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

# }}}
