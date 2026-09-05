import dados


def find_available_equipment(needed_type, equipment_list):
    for item in equipment_list:
        if item["type"] == needed_type and item["busy"] == False:
            return item
    return None


from datetime import datetime, timedelta


def calculate_departure_time(arrival_time, duration_minute):
    time_obj = datetime.strptime(arrival_time, "%H:%M")
    new_time_obj = time_obj + timedelta(minutes=duration_minute)
    new_time_text = new_time_obj.strftime("%H:%M")
    return new_time_text


def process_truck(truck, equipment_list):
    # Pega o equipamento needed do caminhão
    needed_type = truck["equipment_needed"]
    plate = truck["license_plate"]

    available_equipment = find_available_equipment(needed_type, equipment_list)

    # Se achou equipamento, resultado não é None
    if available_equipment:
        available_equipment["busy"] = True
        available_equipment["current_truck"] = plate
        # Calcula o horário de saída, hora de chegada e duração do trabalho
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
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    # CONTANDO CAMINHÕES ATENDIDOS
    served_count = 0
    waiting_count = 0
    total_duration = 0

    for truck in dados.trucks:
        # Se não conseguiu caminhão (Departure_time é None)
        if truck["departure_time"] is not None:
            served_count += 1
            total_duration += truck["service_duration"]
        else:
            waiting_count += 1

    if served_count > 0:
        average_duration = total_duration / served_count
    else:
        average_duration = 0

    print(f"served trucks: {served_count}")
    print(f"waiting trucks: {waiting_count}")
    print(f"total trucks: {served_count + waiting_count}")
    print(f"total duration sum: {total_duration}")
    print(f"average service time: {average_duration:.1f}")


# Encontrando o equipamento pelo ID
def find_equipment_by_id(equipment_id, equipment_list):
    for item in equipment_list:
        if item["equipment_id"] == equipment_id:
            return item
    return None


def release_equipment(equipment_id, equipment_list):
    equipment = find_equipment_by_id(equipment_id, equipment_list)
    equipment["busy"] = False
    equipment["current_truck"] = None


def find_next_waiting_truck(needed_type, trucks_list):
    for truck in trucks_list:
        if truck["departure_time"] is None and truck["equipment_needed"] == needed_type:
            return truck
    return None


def process_queue_after_release(equipment_id, equipment_list, trucks_list):
    release_equipment(equipment_id, equipment_list)
    equipment = find_equipment_by_id(equipment_id, equipment_list)
    needed_type = equipment["type"]
    next_truck = find_next_waiting_truck(needed_type, trucks_list)

    if next_truck:
        print(f" Found Truck {next_truck['license_plate']} waiting for {needed_type}")
        process_truck(next_truck, equipment_list)
