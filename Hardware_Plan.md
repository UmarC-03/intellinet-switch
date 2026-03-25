# IntelliNet Switch – Hardware Plan

## 1. Project Objective
The **IntelliNet Switch** is a dedicated, high-performance network appliance built on a Raspberry Pi. It aggregates multiple internet uplinks (WiFi + Ethernet) and uses a custom scoring engine to provide a single, ultra-stable "Clean LAN" output to a host machine, ensuring zero-drop connectivity for gaming, streaming, or professional development.

---

## 2. System Architecture
The system acts as an intelligent bridge between various unstable internet sources and the end-user device.

### Hardware Workflow
* **Input A:** WiFi 802.11ac/ax (Wireless Uplink)
* **Input B:** Ethernet / WAN (Wired Uplink via USB Adapter)
* **Processing:** Raspberry Pi (Logic & Routing Engine)
* **Output:** Dedicated LAN (Onboard RJ45 to PC)

---

## 3. Full Hardware List

### 3.1 Computing Unit: Raspberry Pi 5 (4GB or 8GB)
The "Brain" of the IntelliNet Switch.
* **Role:** Runs the custom IntelliNet Linux environment and performs network scoring.
* **Requirement:** Raspberry Pi 5 is preferred for superior I/O throughput; Pi 4B (4GB+) is a valid alternative.
* **Quantity:** 1

### 3.2 Ethernet Expansion: USB 3.0 to Gigabit Ethernet Adapter
* **Role:** Adds the second physical Ethernet port required for dual-wired capability.
* **Requirement:** Must be **USB 3.0** (Gigabit rated). USB 2.0 adapters will throttle speeds to 100Mbps.
* **Quantity:** 1

### 3.3 Network Cables: 2x Cat6 Ethernet Cables
* **Role:**  * **Cable 1:** Wired Internet Input (Modem/Router) → Pi.
  * **Cable 2:** Clean Output (Pi) → User PC.
* **Requirement:** **Cat6** for maximum shielding and interference reduction.
* **Quantity:** 2 (1–2 meters each).

### 3.4 Power Delivery: Official Raspberry Pi 27W USB-C Power Supply
* **Role:** Provides stable 5.1V / 5.0A power to the Pi and all attached USB peripherals.
* **Note:** Using a standard phone charger often causes "Under-voltage" instability during heavy network switching.
* **Quantity:** 1

### 3.5 Storage: 32GB or 64GB MicroSD Card (Class 10 / A1)
* **Role:** Stores the Raspberry Pi OS Lite and the `main.py` IntelliNet logic.
* **Requirement:** Must be **A1 or A2 rated** for high-speed script execution.
* **Quantity:** 1

### 3.6 Thermal Management: Active Cooler (Fan + Heatsink)
* **Role:** Prevents CPU throttling during intensive real-time metric calculations.
* **Quantity:** 1

---

## 4. Logical Connectivity Map

```text
[ SOURCE 1: WiFi ] --------+
                           |
                           v
[ SOURCE 2: USB-ETH ] --> [ RASPBERRY PI ] --> [ ONBOARD ETH0 ] --> [ USER PC ]
  (Internet Input)        (IntelliNet OS)       (Clean Output)
