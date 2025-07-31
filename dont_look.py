import random
import subprocess
import time


web_sites = ["",""]

vpns = ["kua", "and", "bue", "sof", "fra", "sin"]

for index in range(500):
    website = random.choice(web_sites)
    vpn = random.choice(vpns)

    print("connecting to ", vpn)
    subprocess.run(["sudo", "nmcli", "con", "up", vpn])
    time.sleep(3)

    print("Opening ", website)
    subprocess.Popen(["/usr/bin/firefox", "--new-window", website])
    wait_time = 15 + random.randint(0, 5)
    print("Waiting for ", wait_time)
    time.sleep(7)
    subprocess.run(["sudo", "ydotool", "click", "0"])
    time.sleep(wait_time)
    print("killing")
    if index % 5 == 0 and index > 0:
        subprocess.run(["killall", "-15", "firefox"])
    print("removing vpn")
    subprocess.run(["sudo", "nmcli", "con", "down", vpn])