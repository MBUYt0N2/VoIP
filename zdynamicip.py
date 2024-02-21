import subprocess


def get_server_ip():
    try:
        output = subprocess.check_output("ifconfig | grep 192.", shell=True).decode()
    except:
        output = subprocess.check_output("ifconfig | grep 10.", shell=True).decode()
    lines = output.split(" ")
    for i in lines:
        if "192." in i or "10." in i:
            serverip = i.strip()
            break
    return serverip

print(get_server_ip())