
"""
 ==================================
 main.py - Truck Management System
 ==================================

Entry point of the Truck Queue Simulator.
 
This script runs a full simulation from start to finish:
  1. Processes every truck in dados.trucks, trying to allocate a matching
     free equipment to each one (some may end up waiting, if no compatible
     equipment is free at that moment).
  2. Prints a report showing how many trucks were served vs. waiting.
  3. Simulates equipment being released (finishing a job), which
     automatically triggers the next waiting truck (FIFO) to be served.
  4. Prints an updated report after each release, so the effect of the
     queue logic is visible step by step.
 
To run:
    python main.py
"""

# Step 1: try to allocate equipment to every truck.
# Trucks that don't find a compatible free equipment will remain waiting
# (their "departure_time" stays None) until an equipment is released later.
import dados
import logica

for truck in dados.trucks:
    logica.process_truck(truck, dados.equipment)

logica.print_report()

# Step 2: simulate equipment 2 (RTG) finishing its job and becoming free.
# This should automatically pick up the next truck waiting for an RTG.
print("\n--- Simulating equipment 2 release ---")
logica.process_queue_after_release(2, dados.equipment, dados.trucks)

print("\n--- Updated report ---")
logica.print_report()

# Step 3: simulate equipment 4 (RS) finishing its job and becoming free.
# This should automatically pick up the next truck waiting for an RS,
# closing the loop so every truck ends up served.
print("\n--- Simulating equipment 4 release ---")
logica.process_queue_after_release(4, dados.equipment, dados.trucks)
print("\n--- Updated report ---")
logica.print_report()
