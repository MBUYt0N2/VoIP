import subprocess
import os

def get_server_ip():

    if os.name == "posix":
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
    
    elif os.name == "nt":
        output = subprocess.check_output("ipconfig", shell=True).decode()
        lines = output.split('\n')
	flag = 0
        for line in lines:
		if "Wi-Fi" in line:
			flag = 1
		if "IPv4 Address" in line and flag == 1:
        	        serverip = line.split(":")[1].strip()
                	return serverip

