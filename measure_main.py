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
result[0]={"all_energy":0}


def create_result_name():
    time_to_name = time.gmtime()
    name_file = f"{time_to_name.tm_year}_{time_to_name.tm_mon}_{time_to_name.tm_mday}_{time_to_name.tm_hour + 2}_{time_to_name.tm_min}"
    return name_file


def main():
    count = 0 
    while 1:
        time.sleep(perioud)
        count+=1
        ram = technical_recorder.ram_measure()
        a = (a_measure.main())/1000
        p = a*v
        w_temp = p*perioud
        w_all = w_temp + result[count-1]["all_energy"]
        measure_time = time.time() - start_time
        result[count]={"current": a, "voltage": v, "power": p, "energy_in_perioud": w_temp, "all_energy": w_all, "measure_time": measure_time, "RAM using %": ram}
        print(result[count])
        if result[count]["current"] < 0.1:
            output_name = create_result_name()
            os.mkdir(f"results/{output_name}")
            with open(f"results/{output_name}/report.json", "w") as outfile:
                json.dump(result, outfile)
            break

if __name__ == "__main__":
    main()
