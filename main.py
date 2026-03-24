import random
import time

# --- Configuration ---
print("====== INTELLINET SWITCH ======")
current_network = str(input("Enter current network (WiFi/Hotspot): ")).strip().lower()
intervel = int(input("Enter interval (seconds): "))
threshold = float(input("Enter metric threshold: "))
print("\n--- SELECT PRIMARY METRIC ---")
print("1. Latency (ms)")
print("2. Packet Loss (%)")
print("3. Throughput (Mbps)")
choice = input("Select (1/2/3): ")

metric_map = {"1": "Latency", "2": "Packet Loss", "3": "Mbps"}
selected_metric = metric_map.get(choice, "Latency")

print("================================")

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

# --- Main Loop ---
while True:
    wifi_latency, wifi_packet_loss, wifi_throughput = get_wifi_metrics()
    hotspot_latency, hotspot_packet_loss, hotspot_throughput = get_hotspot_metrics()
    if selected_metric == "Latency":
        w_val, h_val = wifi_latency, hotspot_latency
        unit = "ms"
    elif selected_metric == "Packet Loss":
        w_val, h_val = wifi_packet_loss, hotspot_packet_loss
        unit = "%"
    else: # Mbps
        w_val, h_val = wifi_throughput, hotspot_throughput
        unit = "Mbps"

    print(f"WiFi {selected_metric}: {round(w_val, 1)}{unit} | Hotspot {selected_metric}: {round(h_val, 1)}{unit} | Active: {current_network}")

    if current_network == "wifi":

        if selected_metric == "Mbps":
            if h_val - w_val > threshold:
                network_hotspot()
                print(f"Switching to Hotspot due to better {selected_metric}.")
        else:
            if w_val - h_val > threshold:
                network_hotspot()
                print(f"Switching to Hotspot due to poor {selected_metric}.")

    elif current_network == "hotspot":
        
        if selected_metric == "Mbps":
            if w_val - h_val > threshold:
                network_wifi()
                print(f"Switching to WiFi due to better {selected_metric}.")
        else:
            if h_val - w_val > threshold:
                network_wifi()
                print(f"Switching to WiFi due to poor {selected_metric}.")

    print("-" * 30)
    time.sleep(intervel)