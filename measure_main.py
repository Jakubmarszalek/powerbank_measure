import time
import ina219
import json
import os 

import a_measure
import technical_recorder

perioud = 2
v=5
start_time = time.time()
result = {}


def create_result_name():
    time_to_name = time.gmtime()
    name_file = f"{time_to_name.tm_year}_{time_to_name.tm_mon}_{time_to_name.tm_mday}_{time_to_name.tm_hour + 2}_{time_to_name.tm_min}_{time_to_name.tm_sec}"
    return name_file

def create_report(result):
    number_of_measure = len(result) - 1
    result.pop(number_of_measure + 1)
    current_all = 0
    voltage_all = 0
    power_all = 0
    print(result)

    for measure in result:
        current_all += result[measure]["current"]
        voltage_all += result[measure]["voltage"]
        power_all += result[measure]["power"]
    current_average = current_all/number_of_measure
    voltage_average = voltage_all/number_of_measure
    power_average = power_all/number_of_measure
    all_energy_mAh = result[measure]["all_energy"] / 18
    all_measure_time = result[measure]["measure_time"]
    final_report = {}
    final_report["current_average"] = current_average
    final_report["voltage_average"] = voltage_average
    final_report["power_average"] = power_average
    final_report["all_energy_mAh_5V"] = all_energy_mAh
    final_report["all_energy_Joule"] = result[measure]["all_energy"]
    final_report["measurment_time"] = result[measure]["measure_time"]
    final_report["time_of_finish_measure"] = create_result_name()
    print(final_report)
    return final_report
def main():
    count = 0 
    while 1:
        time.sleep(perioud)
        count+=1
        ram = technical_recorder.ram_measure()
        a = (a_measure.main())/1000
        p = a*v
        w_temp = p*perioud
        if count == 1:
            w_all = w_temp
        else:
            w_all = w_temp + result[count-1]["all_energy"]
        measure_time = time.time() - start_time
        result[count]={"current": a, "voltage": v, "power": p, "energy_in_perioud": w_temp, "all_energy": w_all, "measure_time": measure_time, "RAM using %": ram}
        print(result[count])
        if result[count]["current"] < 0.1:
            output_name = create_result_name()
            os.mkdir(f"results/{output_name}")
            with open(f"results/{output_name}/measure_data.json", "w") as outfile:
                json.dump(result, outfile)
            final_report = create_report(result)
            with open(f"results/{output_name}/final_report.json", "w") as outfile:
                json.dump(final_report, outfile)
            break

if __name__ == "__main__":
    main()
