import random
import time

def get_wifi_ping():
    return random.randint(40, 150)

def get_hotspot_ping():
    return random.randint(50, 120)

def switch_to_hotspot():
    print("Switching to hotspot due to lower latency")

def stay_on_wifi():
    print("Staying on WiFi")

while True:
    wifi_ping = get_wifi_ping()
    hotspot_ping = get_hotspot_ping()

    print(f"WiFi: {wifi_ping}ms | Hotspot: {hotspot_ping}ms")

    if wifi_ping - hotspot_ping > 20:
        switch_to_hotspot()
    else:
        stay_on_wifi()

    print("-" * 30)
    time.sleep(2)