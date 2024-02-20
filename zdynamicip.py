import subprocess


def get_server_ip():
    output = subprocess.check_output("ifconfig | grep 192.", shell=True).decode()
    if output is None:
        output = subprocess.check_output("ifconfig | grep 10.", shell=True).decode()
    lines = output.split(" ")
    for i in lines:
        if "192." in i or "10." in i:
            serverip = i.strip()
            break
    return serverip

