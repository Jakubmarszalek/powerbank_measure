import time
import ina219
import json
import os 
import argparse

import a_measure
import voltage_measure
import technical_recorder
import lcd_screen

with open('config.json') as json_file:
    config_values = json.load(json_file)
perioud = config_values["perioud"]
start_voltage_value = config_values["start_voltage_value"]
start_sleep_perioud = config_values["start_sleep_perioud"]
stop_current_value = config_values["stop_current_value"]
stop_voltage_value = config_values["stop_voltage_value"]
result_folder_name = config_values["result_folder_name"]


result = {}

def create_parser():
    parser = argparse.ArgumentParser('Run behave in parallel mode for scenarios')
    parser.add_argument('--name', '-n', action='store', required=False,
                        help='name of folder with results', default="")
    return parser

def create_result_name(individual_name = None):
    time_to_name = time.gmtime()
    name_file = f"{time_to_name.tm_year}_{time_to_name.tm_mon}_{time_to_name.tm_mday}_{time_to_name.tm_hour + 2}_{time_to_name.tm_min}_{time_to_name.tm_sec}"
    if individual_name:
        name_file = individual_name + name_file
    return name_file


def create_report(result):
    number_of_measure = len(result) - 1
    result.pop(number_of_measure + 1)
    current_all = 0
    voltage_all = 0
    power_all = 0

    for measure in result:
        current_all += result[measure]["current"]
        voltage_all += result[measure]["voltage"]
        power_all += result[measure]["power"]
    current_average = current_all/number_of_measure
    voltage_average = voltage_all/number_of_measure
    power_average = power_all/number_of_measure
    all_energy_mAh = result[measure]["all_energy"] / 18
    all_measure_time = result[measure]["all_measure_time"]
    final_report = {}
    final_report["current_average"] = current_average
    final_report["voltage_average"] = voltage_average
    final_report["power_average"] = power_average
    final_report["all_energy_mAh_5V"] = all_energy_mAh
    final_report["all_energy_Joule"] = result[measure]["all_energy"]
    final_report["all_measurment_time"] = result[measure]["all_measure_time"]
    final_report["time_of_finish_measure"] = create_result_name()
    return final_report


def main():
    parser = create_parser()
    args = parser.parse_args()
    print("Waiting for voltage...")
    lcd_screen.message("Waiting for", "voltage...")
    while 1:
        if voltage_measure.main() > start_voltage_value:
            print(f"Detected voltage bigger then {start_voltage_value}V, measure start:")
            lcd_screen.message("Detected voltage", "measure start")
            break
        time.sleep(start_sleep_perioud)
    count = 0
    start_time = time.time()
    perioud_time = time.time()
    while 1:
        time.sleep(perioud)
        count+=1
        ram = technical_recorder.ram_measure()
        a = (a_measure.main())/1000
        v = voltage_measure.main()
        p = a*v
        one_measure_time = time.time() - perioud_time
        print(one_measure_time)
        perioud_time = time.time()
        w_temp = p * one_measure_time
        if count == 1:
            w_all = w_temp
        else:
            w_all = w_temp + result[count-1]["all_energy"]
        all_measure_time = time.time() - start_time
        result[count]={"current": a, "voltage": v, "power": p, "energy_in_perioud": w_temp, "all_energy": w_all, "all_measure_time": all_measure_time, "RAM using %": ram,
                        "single_measure_time": one_measure_time}
        print(result[count])
        lcd_screen.measure_show(result[count]["voltage"], result[count]["current"], result[count]["all_measure_time"], result[count]["all_energy"]/18)
        if (result[count]["current"] < stop_current_value) or (result[count]["voltage"] < stop_voltage_value):
            output_name = create_result_name(args.name)
            script_localization = os.path.dirname(os.path.realpath(__file__))
            result_path = os.path.join(script_localization, result_folder_name, output_name)
            os.mkdir(result_path)
            with open(os.path.join(result_path, "measure_data.json"), "w") as outfile:
                json.dump(result, outfile)
            final_report = create_report(result)
            print(final_report)
            lcd_screen.final_info(final_report["all_measurment_time"], final_report["all_energy_mAh_5V"])
            with open(os.path.join(result_path, "final_report.json"), "w") as outfile:
                json.dump(final_report, outfile)
            break

if __name__ == "__main__":
    main()
