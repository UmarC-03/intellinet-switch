import random
import time
import math
import psutil
import urllib.request
from ping3 import ping

# --- 1. CONFIGURATION & PROFILES ---
print("====== INTELLINET SWITCH ======")
current_network = str(input("Enter current network (WiFi/Ethernet): ")).strip().lower()
interval = float(input("Enter check interval (seconds): "))
mode = input("Enter mode (sim/real): ").strip().lower()

PROFILES = {
    "1": ("Gaming", {"lat": 0.45, "loss": 0.40, "speed": 0.15}),
    "2": ("Streaming", {"lat": 0.20, "loss": 0.30, "speed": 0.50}),
    "3": ("General", {"lat": 0.35, "loss": 0.35, "speed": 0.30})
}

print("\n--- SELECT PROFILE ---")
for key, (name, _) in PROFILES.items():
    print(f"{key}. {name}")

choice = input("Select (1/2/3): ")
profile_name, weights = PROFILES.get(choice, PROFILES["3"])
print(f"ACTIVE PROFILE: {profile_name}\n" + "="*31)

# --- 2. NORMALIZATION PARAMETERS ---
LAT_REF, SPEED_REF, LOSS_K = 50, 25, 15
HYSTERESIS_MARGIN = 0.12

# --- 3. THE MATH ENGINE ---
def get_score(lat, loss, speed):
    q_lat = 1 / (1 + (lat / LAT_REF)**2)
    q_loss = math.exp(-LOSS_K * (loss / 100))
    q_speed = 1 - math.exp(-speed / SPEED_REF)
      
    if loss >= 100:
        return 0.0
    return (weights["lat"] * q_lat) + (weights["loss"] * q_loss) + (weights["speed"] * q_speed)

def simulate_metrics(net_type):
    if net_type == "wifi":
        lat = random.randint(20, 100)
        loss = random.uniform(0, 5)
        speed = random.uniform(10, 100)
        return lat, loss, speed
    return random.randint(10, 120), random.uniform(0, 5), random.uniform(10, 100)

def get_real_metrics(net_type):
    if net_type == "wifi":
        target = '8.8.8.8'
        samples = 4
        latencies = []
        
        for _ in range(samples):
            try:
                res = ping(target, timeout=1)
                if res is not None:
                    latencies.append(res * 1000)
            except Exception:
                pass
                
        lat = sum(latencies) / len(latencies) if latencies else 999
        loss = ((samples - len(latencies)) / samples) * 100

        test_url = "https://speed.hetzner.de/1MB.bin"
        
        t0 = time.perf_counter()
        io0 = psutil.net_io_counters()
        
        try:
            with urllib.request.urlopen(test_url, timeout=3) as response:
                _ = response.read(256 * 1024) 
        except Exception:
            pass
            
        io1 = psutil.net_io_counters()
        t1 = time.perf_counter()

        time_diff = t1 - t0
        bytes_diff = io1.bytes_recv - io0.bytes_recv
        speed = (bytes_diff * 8 / 1_000_000) / time_diff if time_diff > 0 else 0

        return lat, loss, speed
    return random.randint(10, 120), random.uniform(0, 5), random.uniform(10, 100)  
    #Fallback for ethernet since real metrics are not implemented yet.

def switch_to(target):
    global current_network
    current_network = target
    print(f"ACTION: Switching to {target.upper()}")

if mode == "real":
    get_metrics = get_real_metrics
else:
    get_metrics = simulate_metrics

# --- 4. MAIN AUTONOMOUS LOOP ---
try:
    print("Intellinet Engine Running. Press Ctrl+C to stop.\n" + "="*31)
    while True:
        w_lat, w_loss, w_speed = get_metrics("wifi")
        h_lat, h_loss, h_speed = get_metrics("ethernet")

        w_score = get_score(w_lat, w_loss, w_speed)
        h_score = get_score(h_lat, h_loss, h_speed)
        diff = abs(w_score - h_score)

        if w_loss >= 100: w_score = 0.0
        if h_loss >= 100: h_score = 0.0

        print(f"WiFi: {w_score:.3f} | ethernet: {h_score:.3f} | Active: {current_network}")

        if current_network == "wifi" and h_score > (w_score + HYSTERESIS_MARGIN):
            switch_to("ethernet")
        elif current_network == "ethernet" and w_score > (h_score + HYSTERESIS_MARGIN):
            switch_to("wifi")

        print("-" * 31)
        time.sleep(interval)
except KeyboardInterrupt:
    print("\n[!] Intellinet Engine Stopped.")