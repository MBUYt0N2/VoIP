import subprocess


def get_server_ip():
    output = subprocess.check_output("ifconfig | grep inet", shell=True).decode()
    lines = output.split("\n")
    for i in lines:
        if "192." in i or "10." in i:
            serverip = i.strip().split(" ")[1]
            break
    return serverip
