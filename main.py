import random
import time
import math

# --- 1. CONFIGURATION & PROFILES ---
print("====== INTELLINET SWITCH ======")
current_network = str(input("Enter current network (WiFi/ethernet): ")).strip().lower()
interval = float(input("Enter check interval (seconds): "))

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
    
    return (weights["lat"] * q_lat) + (weights["loss"] * q_loss) + (weights["speed"] * q_speed)

def simulate_metrics(net_type):
    if net_type == "wifi":
        return random.randint(20, 100), random.uniform(0, 5), random.uniform(10, 100)
    return random.randint(50, 120), random.uniform(0, 5), random.uniform(10, 100)

def switch_to(target):
    global current_network
    current_network = target
    print(f"ACTION: Switching to {target.upper()}")

# --- 4. MAIN AUTONOMOUS LOOP ---
try:
    print("Intellinet Engine Running. Press Ctrl+C to stop.\n" + "="*31)
    while True:
        w_lat, w_loss, w_speed = simulate_metrics("wifi")
        h_lat, h_loss, h_speed = simulate_metrics("ethernet")

        w_score = get_score(w_lat, w_loss, w_speed)
        h_score = get_score(h_lat, h_loss, h_speed)
        diff = abs(w_score - h_score)

        print(f"WiFi: {w_score:.3f} | ethernet: {h_score:.3f} | Active: {current_network}")

        if current_network == "wifi" and h_score > (w_score + HYSTERESIS_MARGIN):
            switch_to("ethernet")
        elif current_network == "ethernet" and w_score > (h_score + HYSTERESIS_MARGIN):
            switch_to("wifi")

        print("-" * 31)
        time.sleep(interval)
except KeyboardInterrupt:
    print("\n[!] Intellinet Engine Stopped.")