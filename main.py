import random
import time

# --- Configuration ---
print("====== INTELLINET SWITCH ======")
intervel = int(input("Enter interval (seconds): "))
threshold = int(input("Enter latency threshold (ms): "))
current_network = str(input("Enter current network (WiFi/Hotspot): ")).strip().capitalize()
print(current_network)
print("================================")


def get_wifi_ping():
    return random.randint(40, 150)

def get_hotspot_ping():
    return random.randint(50, 120)

def network_hotspot():
    global current_network
    current_network = "Hotspot"

def network_wifi():
    global current_network
    current_network = "WiFi"

while True:
    wifi_ping = get_wifi_ping()
    hotspot_ping = get_hotspot_ping()

    print(f"WiFi: {wifi_ping}ms | Hotspot: {hotspot_ping}ms | Current Network: {current_network}")

    if current_network == "WiFi":
        if wifi_ping - hotspot_ping > threshold:
            network_hotspot()
            print("Switching to Hotspot due to high latency.")
    elif current_network == "Hotspot":
        if hotspot_ping - wifi_ping > threshold:
            network_wifi()
            print("Switching to WiFi due to high latency.")

    print("-" * 30)
    time.sleep(intervel)