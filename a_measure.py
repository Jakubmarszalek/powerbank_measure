import ina219
def main():
	ina = ina219.INA219(shunt_ohms=0.1,
        	max_expected_amps=3,
        	address=0x40)

	ina.configure(voltage_range=ina.RANGE_16V,
              	gain=ina.GAIN_AUTO,
             	bus_adc=ina.ADC_128SAMP,
              	shunt_adc=ina.ADC_128SAMP)

	return ina.current()
if __name__ == "__main__":
	print(main())
