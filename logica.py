"""
logica.py
---------
Business logic for the Truck Queue Simulator.

This module contains all the rules that decide how trucks are matched to
available equipment (RTG or RS), how waiting trucks are queued (FIFO), and
how the final report is calculated.

It depends on `dados.py`, which holds the sample data: the `equipment` list
(available cranes/reach stackers) and the `trucks` list (trucks to be
served).
"""

import dados
from datetime import datetime, timedelta


def find_available_equipment(needed_type, equipment_list):
    for item in equipment_list:
        """
        Look for the first equipment that is both free and of the needed type.

        Parameters:
        needed_type (str): the type of equipment required ("RTG" or "RS").
        equipment_list (list): the list of equipment dictionaries to search.

        Returns:
        dict: the first matching equipment found, still referencing the
        original dictionary (so changes to it affect equipment_list).
        None: if no equipment of that type is currently free.
        """

        if item["type"] == needed_type and item["busy"] == False:
            return item
    return None


def calculate_departure_time(arrival_time, duration_minute):
    """
    Calculate the time a truck will leave, based on arrival time + duration.

    Parameters:
    arrival_time (str): time the truck arrived, in "HH:MM" format.
    duration_minute (int): how many minutes the service takes.

    Returns:
    str: the calculated departure time, in "HH:MM" format.

    Example:
    calculate_departure_time("08:00", 20) -> "08:20"
    """

    time_obj = datetime.strptime(arrival_time, "%H:%M")
    new_time_obj = time_obj + timedelta(minutes=duration_minute)
    new_time_text = new_time_obj.strftime("%H:%M")
    return new_time_text


def process_truck(truck, equipment_list):
    """
    Try to serve a single truck: find a matching free equipment and, if one
    exists, allocate it to this truck and calculate the departure time.

    If no equipment is available, the truck stays in a "waiting" state
    (its "departure_time" field remains None) and a message is printed.

    Parameters:
    truck (dict): the truck to process (from dados.trucks).
    equipment_list (list): the list of equipment to search (from
    dados.equipment).
    """
    needed_type = truck["equipment_needed"]
    plate = truck["license_plate"]

    available_equipment = find_available_equipment(needed_type, equipment_list)

    # If we found a free equipment of the right type, allocate it
    if available_equipment:
        available_equipment["busy"] = True
        available_equipment["current_truck"] = plate
        # Calculate departure time based on arrival + how long service takes
        truck["departure_time"] = calculate_departure_time(
            truck["arrival_time"], truck["service_duration"]
        )
        print(
            f"truck {plate} alocated equipment {available_equipment['equipment_id']} ({needed_type})"
        )
        return True
    else:
        print(f"Truck {plate} waiting, no {needed_type} available.")
        return False


def print_report():
    """
    Print a summary report of the current simulation state:
    - how many trucks were served
    - how many are still waiting
    - total trucks
    - sum and average of service duration (only for served trucks)

    Reads directly from dados.trucks, so it always reflects the latest
    state of the simulation.
    """
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    served_count = 0
    waiting_count = 0
    total_duration = 0

    # Single pass over all trucks: classify each one as served or waiting
    for truck in dados.trucks:
        if truck["departure_time"] is not None:
            served_count += 1
            total_duration += truck["service_duration"]
        else:
            waiting_count += 1

    # Avoid dividing by zero if no truck has been served yet
    if served_count > 0:
        average_duration = total_duration / served_count
    else:
        average_duration = 0

    print(f"served trucks: {served_count}")
    print(f"waiting trucks: {waiting_count}")
    print(f"total trucks: {served_count + waiting_count}")
    print(f"total duration sum: {total_duration}")
    print(f"average service time: {average_duration:.1f}")


def find_equipment_by_id(equipment_id, equipment_list):
    """
    Find a specific equipment by its id.

    Parameters:
    equipment_id (int): the id to search for.
    equipment_list (list): the list of equipment dictionaries.

    Returns:
    dict: the equipment dictionary with that id, if found.
    None: if no equipment with that id exists.
    """
    for item in equipment_list:
        if item["equipment_id"] == equipment_id:
            return item
    return None


def release_equipment(equipment_id, equipment_list):
    """
    Mark a specific equipment as free again (simulates it finishing a job).

    Parameters:
    equipment_id (int): the id of the equipment to release.
    equipment_list (list): the list of equipment dictionaries.
    """
    equipment = find_equipment_by_id(equipment_id, equipment_list)
    equipment["busy"] = False
    equipment["current_truck"] = None


def find_next_waiting_truck(needed_type, trucks_list):
    """
    Find the first truck in the list that is still waiting (has not been
    served yet) and needs a specific type of equipment. This enforces a
    FIFO (First In, First Out) order, since we always return the first
    match found in the list.

    Parameters:
    needed_type (str): the equipment type to match ("RTG" or "RS").
    trucks_list (list): the list of truck dictionaries.

    Returns:
    dict: the first waiting truck that needs this equipment type.
    None: if no truck is waiting for this type.
    """
    for truck in trucks_list:
        if truck["departure_time"] is None and truck["equipment_needed"] == needed_type:
            return truck
    return None


def process_queue_after_release(equipment_id, equipment_list, trucks_list):
    """
    Simulate an equipment finishing its current job and automatically
    serving the next compatible truck in the waiting queue, if any.

    Steps:
    1. Release the given equipment (mark it as free).
    2. Find out what type of equipment it is.
    3. Look for the next waiting truck that needs that type.
    4. If found, process that truck immediately (allocate the
    equipment that just became free).

    Parameters:
    equipment_id (int): the id of the equipment that just finished.
    equipment_list (list): the list of equipment dictionaries.
    trucks_list (list): the list of truck dictionaries.
    """
    release_equipment(equipment_id, equipment_list)
    equipment = find_equipment_by_id(equipment_id, equipment_list)
    needed_type = equipment["type"]
    next_truck = find_next_waiting_truck(needed_type, trucks_list)

    if next_truck:
        print(f" Found Truck {next_truck['license_plate']} waiting for {needed_type}")
        process_truck(next_truck, equipment_list)
