# Intellinet Switch

An autonomous network selection engine designed to solve connection instability by prioritizing objective health over simple signal strength. This system moves beyond standard OS switching by evaluating the relationship between latency, packet loss, and throughput in real-time.

The core of the project is a weighted decision machine that utilizes non-linear normalization to determine the "Net Health" of a connection, ensuring data-heavy or latency-sensitive tasks remain on the most stable interface available.


## Hardware Architecture

The Intellinet Switch is designed to operate as a physical intermediary device. A user's computer connects directly to the Switch (via Ethernet or high-speed bridge), which then manages multiple upstream backhauls (such as Fiber, LTE, or Starlink).

By controlling the physical layer through Raspberry Pi GPIO and relay modules, the device can swap the primary internet source in milliseconds. This ensures the end-user’s computer maintains a persistent, "never-drop" connection, even if an individual upstream provider fails entirely.


## Technical Architecture

The system operates on a multi-layered evaluation logic:

1. **Normalization Layer:** Raw metrics (ms, %, Mbps) are converted into a standardized 0.0 to 1.0 scale. This allows the engine to compare "apples to oranges" accurately.
2. **Exponential Decay:** The engine treats packet loss as a critical failure point. Using exponential functions, even a 1% increase in loss aggressively drops the network's health score.
3. **Weighting Profiles:** Users select a logic profile (Gaming, Streaming, or General) that shifts the engine's priorities. Gaming profiles favor low latency, while Streaming profiles favor raw throughput.
4. **Hysteresis Buffer:** To prevent "switch-spam," the engine requires the alternative network to be at least 12% better than the current one before triggering a transition.

---

## Dev Log

**Day 1:**
- Established core latency simulation and basic switching logic.

**Day 2:**
- Implemented State-Aware Logic to prevent redundant toggling.
- Introduced User Configuration for interval and threshold management.

**Day 3:**
- Expanded monitoring to include Packet Loss and Mbps.
- Refined decision logic to handle inverse metrics (where higher Mbps is better, but higher Latency is worse).

**Day 4:**
- Developed the Autonomous Intelligence Engine, removing manual metric selection.
- Integrated Mathematical Normalization.
- Implemented Profile-Based Weighting optimization.

## Future Roadmap

- **Interface Integration:** Replace simulated values with live system subprocess pings and speed tests.
- **Hardware Triggering:** Map software decisions to physical GPIO pins for Raspberry Pi relay switching.
- **Visual Interface:** Develop a high-contrast terminal dashboard for real-time score tracking.

## Usage Notice

All code and concepts in this repository are proprietary. No permission is granted to copy, modify, distribute, sublicense, or use this project or its underlying concept for commercial or non-commercial purposes without explicit written permission from the author.

Copyright (c) 2026 Umar Coovadia
