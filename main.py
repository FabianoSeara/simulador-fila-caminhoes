# ==================================
# main.py - Truck Management System
# ==================================

import dados
import logica

for truck in dados.trucks:
    logica.process_truck(truck, dados.equipment)

logica.print_report()


print("\n--- Simulating equipment 2 release ---")
logica.process_queue_after_release(2, dados.equipment, dados.trucks)
print("\n--- Updated report ---")
logica.print_report()


print("\n--- Simulating equipment 4 release ---")
logica.process_queue_after_release(4, dados.equipment, dados.trucks)
print("\n--- Updated report ---")
logica.print_report()
