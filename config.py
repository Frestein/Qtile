# vim:fileencoding=utf-8:foldmethod=marker
from os import environ, path
from subprocess import Popen

from libqtile import bar, extension, hook, qtile
from libqtile.backend.wayland import InputConfig
from libqtile.config import DropDown, Group, Match, ScratchPad, Screen
from libqtile.config import EzClick as Click
from libqtile.config import EzDrag as Drag
from libqtile.config import EzKey as Key
from libqtile.config import EzKeyChord as KeyChord
from libqtile.layout import Bsp, Columns, Floating, Max, Stack, Tile
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from utils.audio import get_active_audio_device

# Variables {{{

home = path.expanduser("~")

terminal = ""

if qtile.core.name == "x11":
    terminal = "st"
elif qtile.core.name == "wayland":
    terminal = "foot"

autostart_sh = home + "/.config/qtile/scripts/qtile_autostart"
color_picker = home + "/.config/qtile/scripts/qtile_colorpicker"
network_manager = home + "/.config/qtile/scripts/networkmanager"
websearch = home + "/.config/qtile/scripts/dmenu_websearch"
download = home + "/.config/qtile/scripts/dmenu_downloader"
volume = home + "/.config/qtile/scripts/qtile_volume"
screenshot = home + "/.config/qtile/scripts/qtile_screenshot"
file_manager = "nemo"
tui_file_manager = home + "/.cargo/bin/yazi"
web_browser = "firefox"
terminal_session = "kitty --session=session.conf"
tabbed_terminal = "tabbed -c -r 2 st -w ''"
email_client = "thunderbird"
calculator = "galculator"
android_studio = "android-studio"
upgrade_system = "paru -Syu"
telegram = "telegram-desktop"
password_manager = "keepassxc"
dmenu_applets = home + "/.config/qtile/scripts/"
notify_cmd = "dunstify -u low -h string:x-dunst-stack-tag:qtileconfig"

font_name = "JetBrainsMono Nerd Font Mono"
border_width = 2
margin = 5
colors = [
    "#2E3440",  # 0
    "#3B4252",  # 1
    "#434C5E",  # 2
    "#4C566A",  # 3
    "#D8DEE9",  # 4
    "#E5E9F0",  # 5
    "#ECEFF4",  # 6
    "#8FBCBB",  # 7
    "#88C0D0",  # 8
    "#81A1C1",  # 9
    "#5E81AC",  # 10
    "#BF616A",  # 11
    "#D08770",  # 12
    "#EBCB8B",  # 13
    "#A3BE8C",  # 14
    "#B48EAD",  # 15
    # Extra
    "#333945",  # 16
]

# }}}
# Environments {{{

environ["KITTY_CONFIG_DIRECTORY"] = home + "/.config/qtile/kitty"

# }}}
# Wayland Input Rules {{{

wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_layout="us,ru",
        kb_options="grp:win_space_toggle",
    ),
}


# }}}
# Autostart {{{


@hook.subscribe.startup_once
def autostart():
    Popen([autostart_sh])


# }}}
# Key Bindings {{{

keys = [
    # Apps --
    Key("M-<Return>", lazy.spawn(terminal), desc="Terminal"),
    Key("M-b", lazy.spawn(tabbed_terminal), desc="Tabbed terminal"),
    Key("M-k", lazy.spawn(terminal_session), desc="Terminal session"),
    Key("<XF86HomePage>", lazy.spawn(web_browser), desc="Web browser"),
    Key("<XF86Explorer>", lazy.spawn(file_manager), desc="File manager (GUI)"),
    Key("M-a", lazy.spawn(android_studio), desc="Android Studio"),
    # Scratchpads --
    Key(
        "M-t",
        lazy.group["scratchpad"].dropdown_toggle("Terminal"),
        desc="Dropdown terminal",
    ),
    Key("M-m", lazy.group["scratchpad"].dropdown_toggle("Telegram"), desc="Telegram"),
    Key(
        "M-u",
        lazy.group["scratchpad"].dropdown_toggle("Upgrade system"),
        desc="Upgrade system",
    ),
    Key(
        "<XF86Tools>",
        lazy.group["scratchpad"].dropdown_toggle("Music player"),
        desc="Music player",
    ),
    Key(
        "<XF86Mail>",
        lazy.group["scratchpad"].dropdown_toggle("Email client"),
        desc="Email client",
    ),
    Key(
        "M-S-f",
        lazy.group["scratchpad"].dropdown_toggle("File manager"),
        desc="File manager (TUI)",
    ),
    Key(
        "M-p",
        lazy.group["scratchpad"].dropdown_toggle("Password manager"),
        desc="Password manager",
    ),
    Key(
        "<XF86Calculator>",
        lazy.group["scratchpad"].dropdown_toggle("Calculator"),
        desc="Calculator",
    ),
    # Dmenu Applets --
    Key(
        "A-<F1>",
        lazy.run_extension(
            extension.J4DmenuDesktop(
                dmenu_prompt="Apps ",
                dmenu_command="dmenu -vi",
                dmenu_ignorecase=True,
                dmenu_lines=10,
            )
        ),
        desc="Application launcher applet",
    ),
    Key(
        "A-q",
        lazy.run_extension(
            extension.CommandSet(
                dmenu_prompt="Session Manager",
                commands={
                    " Lock": "betterlockscreen --lock --time-format %H:%M",
                    "󰍃 Logout": "qtile cmd-obj -o cmd -f shutdown",
                    " Reload": "qtile cmd-obj -o cmd -f restart",
                    " Reboot": "systemctl reboot",
                    " Shutdown": "systemctl poweroff",
                },
                dmenu_command="dmenu -vi -noi",
                dmenu_lines=10,
            )
        ),
        desc="Session manager applet",
    ),
    Key(
        "A-w",
        lazy.run_extension(
            extension.WindowList(
                dmenu_prompt="Current open windows",
                item_format="{group} {window}",
                dmenu_command="dmenu -vi -noi",
                dmenu_lines=10,
            )
        ),
        desc="Current open window list applet",
    ),
    Key(
        "A-r",
        lazy.run_extension(
            extension.CommandSet(
                dmenu_prompt="Launch as root",
                commands={
                    " Terminal": dmenu_applets + "qtile_asroot " + terminal,
                    " Neovim": dmenu_applets
                    + 'qtile_asroot "'
                    + terminal
                    + ' -e nvim"',
                    "󰇥 Yazi": dmenu_applets
                    + 'qtile_asroot "'
                    + terminal
                    + " -e "
                    + tui_file_manager
                    + '"',
                    " Nemo": dmenu_applets
                    + 'qtile_asroot "dbus-run-session '
                    + file_manager
                    + '"',
                },
                dmenu_command="dmenu -vi -noi",
                dmenu_lines=10,
            )
        ),
        desc="Asroot applet",
    ),
    Key(
        "M-r",
        lazy.run_extension(
            extension.DmenuRun(
                dmenu_prompt="󰜎 ",
                dmenu_command="dmenu_run -vi",
                dmenu_ignorecase=True,
                dmenu_lines=10,
            )
        ),
        desc="Application runner applet",
    ),
    Key(
        "A-s",
        lazy.spawn(dmenu_applets + "dmenu_screenshot"),
        desc="Screenshot applet",
    ),
    Key(
        "M-s",
        lazy.spawn(dmenu_applets + "dmenu_websearch"),
        lazy.group["3"].toscreen(),
        desc="Web search applet",
    ),
    Key(
        "A-n",
        lazy.run_extension(
            extension.Dmenu(
                dmenu_command=network_manager,
            )
        ),
        desc="Network manager applet",
    ),
    Key(
        "A-d",
        lazy.spawn(dmenu_applets + "dmenu_downloader"),
        desc="Downloader applet",
    ),
    # Function keys : Volume --
    Key(
        "<XF86AudioRaiseVolume>",
        lazy.spawn(volume + " --inc"),
        desc="Raise speaker volume",
    ),
    Key(
        "<XF86AudioLowerVolume>",
        lazy.spawn(volume + " --dec"),
        desc="Lower speaker volume",
    ),
    Key("<XF86AudioMute>", lazy.spawn(volume + " --toggle"), desc="Toggle mute"),
    # Function keys : Media --
    Key("<XF86AudioNext>", lazy.spawn("playerctl next"), desc="Next track"),
    Key("<XF86AudioPrev>", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key(
        "<XF86AudioPlay>", lazy.spawn("playerctl play-pause"), desc="Toggle play/pause"
    ),
    Key("<XF86AudioStop>", lazy.spawn("playerctl stop"), desc="Stop playing"),
    # Screenshots --
    Key("<Print>", lazy.spawn(screenshot + " --now"), desc="Take Screenshot"),
    Key(
        "C-<Print>",
        lazy.spawn(screenshot + " --in5"),
        desc="Take Screenshot in 5 seconds",
    ),
    Key(
        "S-<Print>",
        lazy.spawn(screenshot + " --in10"),
        desc="Take Screenshot in 10 seconds",
    ),
    Key(
        "C-S-<Print>",
        lazy.spawn(screenshot + " --win"),
        desc="Take Screenshot of active window",
    ),
    Key(
        "M-<Print>",
        lazy.spawn(screenshot + " --area"),
        desc="Take Screenshot of selected area",
    ),
    # Misc --
    Key("A-p", lazy.spawn(color_picker), desc="Run colorpicker"),
    Key(
        "A-C-l",
        lazy.spawn("betterlockscreen --lock --time-format %H:%M"),
        desc="Run lockscreen",
    ),
    # WM Specific --
    Key("M-c", lazy.window.kill(), desc="Kill focused window"),
    # Control Qtile
    Key(
        "M-C-r",
        lazy.reload_config(),
        lazy.spawn(notify_cmd + ' "Configuration Reloaded!"'),
        desc="Reload the config",
    ),
    Key(
        "M-C-s",
        lazy.restart(),
        lazy.spawn(notify_cmd + ' "Restarting Qtile..."'),
        desc="Restart Qtile",
    ),
    Key(
        "M-C-q",
        lazy.shutdown(),
        lazy.spawn(notify_cmd + ' "Exiting Qtile..."'),
        desc="Shutdown Qtile",
    ),
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
    Key(
        "M-z",
        lazy.window.toggle_floating(),
        desc="Put the focused window to/from floating mode",
    ),
    Key(
        "M-f",
        lazy.window.toggle_fullscreen(),
        desc="Put the focused window to/from fullscreen mode",
    ),
    # Go to next/prev group
    Key(
        "C-A-<bracketright>",
        lazy.screen.next_group(skip_empty=1),
        desc="Move to the group on the right",
    ),
    Key(
        "C-A-<bracketleft>",
        lazy.screen.prev_group(skip_empty=1),
        desc="Move to the group on the left",
    ),
    # Back-n-forth groups
    Key("A-<Tab>", lazy.screen.toggle_group(), desc="Move to the last visited group"),
    # Change focus to other window
    Key("M-<Tab>", lazy.layout.next(), desc="Move window focus to other window"),
    # Toggle between different layouts as defined below
    Key("M-S-<space>", lazy.next_layout(), desc="Toggle between layouts"),
    # Increase the space for master window at the expense of slave windows
    Key(
        "M-<equal>",
        lazy.layout.increase_ratio(),
        desc="Increase the space for master window",
    ),
    # Decrease the space for master window in the advantage of slave windows
    Key(
        "M-<minus>",
        lazy.layout.decrease_ratio(),
        desc="Decrease the space for master window",
    ),
    # Toggle between split and unsplit sides of stack.
    Key(
        "M-S-s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
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
        [Key("<Left>", lazy.prev_layout()), Key("<Right>", lazy.next_layout())],
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
    Click("<Button10>", lazy.spawn("playerctl play-pause")),
]

# }}}
# Groups {{{


# Auto-switching group when a new window is launched
@hook.subscribe.client_managed
def auto_switch(window):
    if window.group.name != qtile.current_group.name:
        window.group.cmd_toscreen()


groups = [
    ScratchPad(
        name="scratchpad",
        dropdowns=[
            DropDown(
                "Terminal",
                terminal,
                x=0.5 / 2,
                y=0.5 / 2,
                width=0.5,
                height=0.5,
                opacity=1.0,
            ),
            DropDown(
                "Upgrade system",
                terminal + " -e " + upgrade_system,
                x=0.5 / 2,
                y=0.5 / 2,
                width=0.5,
                height=0.5,
                opacity=1.0,
            ),
            DropDown(
                "Music player",
                terminal + " -n st-cmus -e cmus",
                x=0.5 / 2,
                y=0.5 / 2,
                width=0.5,
                height=0.5,
                opacity=1.0,
            ),
            DropDown(
                "File manager",
                terminal + " -e " + tui_file_manager,
                x=0.5 / 2,
                y=0.5 / 2,
                width=0.5,
                height=0.5,
                opacity=1.0,
            ),
            DropDown(
                "Calculator",
                calculator,
                x=0.75 / 2,
                y=0.75 / 2,
                width=0.25,
                height=0.25,
                opacity=1.0,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "Email client",
                email_client,
                x=0.25 / 2,
                y=0.25 / 2,
                width=0.75,
                height=0.75,
                opacity=1.0,
            ),
            DropDown(
                "Telegram",
                telegram,
                x=0.25 / 2,
                y=0.25 / 2,
                width=0.75,
                height=0.75,
                opacity=1.0,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "Password manager",
                password_manager,
                x=0.25 / 2,
                y=0.25 / 2,
                width=0.75,
                height=0.75,
                opacity=1.0,
            ),
        ],
    ),
    Group(
        name="1",
        matches=[
            Match(wm_class="kitty"),
        ],
        layout="tile",
        label="",
    ),
    Group(
        name="2",
        matches=[
            Match(wm_class="jetbrains-studio"),
            Match(title="JetBrains Toolbox"),
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
        layout="tile",
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
        ],
        label="",
    ),
    Group(
        name="9",
        matches=[
            Match(wm_class="steam"),
            Match(wm_class="lutris"),
        ],
        label="",
    ),
]

for i in groups:
    if not isinstance(i, ScratchPad):
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
# Layouts {{{

layouts = [
    # Extension of the Stack layout
    Columns(
        border_focus=colors[9],
        border_normal=colors[0],
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
    Bsp(
        border_focus=colors[9],
        border_normal=colors[0],
        border_on_single=False,
        border_width=border_width,
        fair=True,
        grow_amount=10,
        lower_right=True,
        margin=margin,
        margin_on_single=margin,
        ratio=1.6,
        wrap_clients=False,
    ),
    # Maximized layout
    Max(
        margin=margin,
    ),
    # A layout composed of stacks of windows
    Stack(
        autosplit=False,
        border_focus=colors[9],
        border_normal=colors[0],
        border_width=border_width,
        fair=False,
        margin=margin,
        num_stacks=2,
    ),
    # A layout with two stacks of windows dividing the screen
    Tile(
        add_after_last=False,
        add_on_top=True,
        border_focus=colors[9],
        border_normal=colors[0],
        border_on_single=False,
        border_width=border_width,
        expand=True,
        margin=margin,
        margin_on_single=margin,
        master_length=1,
        master_match=None,
        max_ratio=0.85,
        min_ratio=0.15,
        ratio=0.618,
        ratio_increment=0.05,
        shift_windows=False,
    ),
    # Floating layout, which does nothing with windows but handles focus order
    Floating(
        border_focus=colors[9],
        border_normal=colors[0],
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
        self.format_options = ["%I:%M", "%m/%d/%Y"]
        self.current_format_index = 0
        self.update_interval = 0.1

    def toggle_format(self):
        self.current_format_index = (self.current_format_index + 1) % len(
            self.format_options
        )
        self.format = self.format_options[self.current_format_index]


decor = {
    "decorations": [RectDecoration(colour=colors[16], radius=0, filled=True)],
    "padding": 20,
}

widget_defaults = dict(
    font=font_name,
    fontsize=14,
    padding=10,
    background=colors[0],
    foreground=colors[0],
)

current_layout_icon = widget.CurrentLayoutIcon(
    scale=0.5,
    use_mask=True,
    foreground=colors[9],
    background=colors[1],
)
group_box = widget.GroupBox(
    fontsize=20,
    borderwidth=0,
    disable_drag=True,
    active=colors[5],
    inactive=colors[5],
    hide_unused=True,
    highlight_method="block",
    highlight_color=colors[15],
    this_current_screen_border=colors[9],
    this_screen_border=colors[0],
    urgent_alert_method="line",
    urgent_border=colors[15],
    urgent_text=colors[5],
    use_mouse_wheel=True,
)
windowname_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[9],
)
windowname = widget.WindowName(
    scroll=True,
    width=300,
    foreground=colors[9],
)
cmus_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[13],
)
cmus = widget.Cmus(
    **decor,
    format="{play_icon}{artist} — {title}",
    scroll=True,
    width=350,
    noplay_color=colors[13],
    play_color=colors[13],
    foreground=colors[13],
)
volume_icon = widget.TextBox(
    text="󰕾",
    fontsize=20,
    background=colors[9],
)
volume = widget.Volume(
    get_volume_command=f"pactl get-sink-volume {get_active_audio_device()}",
    mute_command=volume + " --toggle",
    volume_app="pavucontrol",
    volume_down_command=volume + " --dec",
    volume_up_command=volume + " --inc",
    foreground=colors[9],
)
net_icon = widget.TextBox(
    text="",
    fontsize=22,
    background=colors[10],
)
net = widget.Net(
    mouse_callbacks={
        "Button1": lazy.run_extension(
            extension.Dmenu(
                dmenu_command=network_manager,
            )
        ),
    },
    format="{down:.0f} {down_suffix:<0}/{up:.0f} {up_suffix:<0}",
    update_interval=5,
    foreground=colors[10],
)
memory_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[12],
)
memory = widget.Memory(
    format="{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
    measure_mem="G",
    foreground=colors[12],
)
cpu_icon = widget.TextBox(
    text="󰍛",
    fontsize=20,
    background=colors[13],
)
cpu = widget.CPU(
    format="{load_percent:.0f}%",
    update_interval=5,
    foreground=colors[13],
)
tray_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[8],
)
tray = ""
if qtile.core.name == "x11":
    tray = widget.Systray(
        padding=5,
        icon_size=18,
    )
elif qtile.core.name == "wayland":
    tray = widget.StatusNotifier(
        padding=5,
        icon_size=18,
    )
clock_icon = widget.TextBox(
    text="",
    fontsize=20,
    background=colors[14],
)
clock = CustomClock(
    format="%I:%M",
    foreground=colors[14],
)

# }}}
# Extensions {{{

extension_defaults = dict(
    font=font_name,
    fontsize=16,
    background=colors[0],
    foreground=colors[5],
    selected_background=colors[9],
    selected_foreground=colors[0],
)

# }}}
# Screens {{{

screens = [
    Screen(
        top=bar.Bar(
            [
                current_layout_icon,
                group_box,
                windowname_icon,
                windowname,
                widget.Spacer(length=bar.STRETCH),
                cmus,
                widget.Spacer(length=bar.STRETCH),
                tray,
                widget.Spacer(length=5),
                volume_icon,
                volume,
                net_icon,
                net,
                memory_icon,
                memory,
                cpu_icon,
                cpu,
                clock_icon,
                clock,
            ],
            size=28,
            background=colors[0],
            margin=[10, 10, 5, 10],
            opacity=1,
        ),
        left=bar.Gap(5),
        right=bar.Gap(5),
        bottom=bar.Gap(5),
        # Set static wallpaper.
        wallpaper=home + "/.config/qtile/theme/wallpaper",
        # Set wallpaper mode to "fill" or "stretch".
        wallpaper_mode="fill",
    )
]

# }}}
# General Configuration Variables {{{

# If a window requests to be fullscreen, it is automatically fullscreened.
# Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = True

# When clicked, should the window be brought to the front or not.
# If this is set to "floating_only", only floating windows will get affected (This sets the X Stack Mode to Above.)
bring_front_click = "floating_only"

# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window.
# When switching focus between screens, If there are no windows in the screen, the cursor will warp to the center of the screen.
cursor_warp = False

# A function which generates group binding hotkeys. It takes a single argument, the DGroups object, and can use that to set up dynamic key bindings.
# A sample implementation is available in 'libqtile/dgroups.py' called `simple_key_binder()`, which will bind groups to "mod+shift+0-10" by default.
dgroups_key_binder = None

# A list of Rule objects which can send windows to various groups based on matching criteria.
dgroups_app_rules = []  # type: list

# The default floating layout to use. This allows you to set custom floating rules among other things if you wish.
floating_layout = Floating(
    border_focus=colors[9],
    border_normal=colors[0],
    border_width=border_width,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class="firefox", title="Library"),
        Match(wm_class="galculator"),
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
