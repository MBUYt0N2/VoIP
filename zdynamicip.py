import subprocess

def get_server_ip():
    output = subprocess.check_output("ifconfig | grep inet", shell=True).decode()
    lines = output.split("\n")
    serverip = lines[5].strip().split(" ")[1]
    return serverip

