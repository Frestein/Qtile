import subprocess


def get_active_audio_device():
    output = subprocess.check_output(["pactl", "get-default-sink"])
    device = output.decode().strip()
    return device
