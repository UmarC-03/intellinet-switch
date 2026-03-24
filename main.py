import random
import time
import math

# --- Configuration ---
print("====== INTELLINET SWITCH ======")
current_network = str(input("Enter current network (WiFi/Hotspot): ")).strip().lower()
intervel = float(input("Enter interval (seconds): "))
print("\n--- SELECT PROFILE ---")
print("1. Gaming")
print("2. Streaming")
print("3. General")

profile_choice = input("Select (1/2/3): ")

profile_map = {
    "1": "gaming",
    "2": "streaming",
    "3": "general"
}

selected_profile = profile_map.get(profile_choice, "general")

print("================================")

# --- Normalization Parameters ---
LATENCY_REF = 50
THROUGHPUT_REF = 25
PACKET_LOSS_K = 15

HYSTERESIS_MARGIN = 0.12

WEIGHTS = {

    "gaming": {
        "latency": 0.45,
        "packet_loss": 0.40,
        "throughput": 0.15
    },

    "streaming": {
        "latency": 0.20,
        "packet_loss": 0.30,
        "throughput": 0.50
    },

    "general": {
        "latency": 0.35,
        "packet_loss": 0.35,
        "throughput": 0.30
    }
}

# --- Logic Engine ---
def normalize_latency(latency):
    ratio = latency / LATENCY_REF
    return 1 / (1 + ratio**2)


def normalize_packet_loss(packet_loss):
    P = packet_loss / 100
    return math.exp(-PACKET_LOSS_K * P)


def normalize_throughput(throughput):
    return 1 - math.exp(-throughput / THROUGHPUT_REF)

def compute_score(latency, packet_loss, throughput, profile):
    w = WEIGHTS[profile]
    q_latency = normalize_latency(latency)
    q_loss = normalize_packet_loss(packet_loss)
    q_throughput = normalize_throughput(throughput)
    score = (
        w["latency"] * q_latency
        + w["packet_loss"] * q_loss
        + w["throughput"] * q_throughput
    )
    return score

# --- Monitoring & Swapping ---
# Note: The metric values are simulated for the current prototype.
def get_wifi_metrics():
    latency = random.randint(20, 100)
    packet_loss = random.uniform(0, 5)
    throughput = random.uniform(10, 100)
    return latency, packet_loss, throughput

def get_hotspot_metrics():
    latency = random.randint(50, 120)
    packet_loss = random.uniform(0, 5)
    throughput = random.uniform(10, 100)
    return latency, packet_loss, throughput

def network_hotspot():
    global current_network
    current_network = "hotspot"

def network_wifi():
    global current_network
    current_network = "wifi"

last_score_wifi = 0
last_score_hotspot = 0

# --- Main Loop ---
while True:

    wifi_latency, wifi_packet_loss, wifi_throughput = get_wifi_metrics()

    hotspot_latency, hotspot_packet_loss, hotspot_throughput = get_hotspot_metrics()

    wifi_score = compute_score(
        wifi_latency,
        wifi_packet_loss,
        wifi_throughput,
        selected_profile
    )


    hotspot_score = compute_score(
        hotspot_latency,
        hotspot_packet_loss,
        hotspot_throughput,
        selected_profile
    )


    print(
        f"WiFi Score: {round(wifi_score,3)} | "
        f"Hotspot Score: {round(hotspot_score,3)} | "
        f"Active: {current_network}"
    )

    score_difference = abs(wifi_score - hotspot_score)

    if current_network == "wifi":
        if (
            hotspot_score > wifi_score
            and score_difference > HYSTERESIS_MARGIN
        ):
            network_hotspot()
            print("Switching to Hotspot")


    elif current_network == "hotspot":
        if (
            wifi_score > hotspot_score
            and score_difference > HYSTERESIS_MARGIN
        ):
            network_wifi()
            print("Switching to WiFi)")

    print("-" * 30)
    time.sleep(intervel)