import time
import ina219
import json

import a_measure

perioud = 2
v=5
start_time = time.time()
result = {}
result[0]={"all_energy":0}
count = 0
while 1:
	time.sleep(perioud)
	count+=1
	a = (a_measure.main())/1000
	p = a*v
	w_temp = p*perioud
	w_all = w_temp + result[count-1]["all_energy"]
	measure_time = time.time() - start_time
	result[count]={"current": a, "voltage": v, "power": p, "energy_in_perioud": w_temp, "all_energy": w_all, "measure_time": measure_time}
	print(result[count])
	if result[count]["current"] < 0.1:
		break
