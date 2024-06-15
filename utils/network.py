import subprocess


def get_active_interface():
    output = subprocess.check_output(["ip", "route", "get", "8.8.8.8"])
    interface = output.decode().split("dev ")[1].split(" ")[0]
    return interface
