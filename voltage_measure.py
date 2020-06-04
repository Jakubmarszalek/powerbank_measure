import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

voltage_pin = 0
v_ref = 5.1
bit_convertion = v_ref/1024
voltage_lost_factor = 0.93

def main():
    bit_voltage_value = mcp.read_adc(voltage_pin)
    voltage_value = bit_voltage_value * bit_convertion
    voltage_value = voltage_value / voltage_lost_factor
    return voltage_value

if __name__ == "__main__":
    main()

