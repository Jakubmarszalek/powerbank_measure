import time
from Adafruit_CharLCD import Adafruit_CharLCD
lcd = Adafruit_CharLCD(rs=21, en=20, d4=16, d5=12, d6=7, d7=26,
                       cols=16, lines=2)
lcd_length = 16


def measure_show(voltage, current, m_time, energy):
    voltage = str(voltage)[:6]
    current =str(current)[:6]
    m_time = str(m_time)[:5]
    energy = str(energy)[:5]
    lcd.clear()
    lcd.message(f"{voltage}V {current}A\n{m_time}s {energy}mAh")


def message(first_line, secound_line=None):
    if len(first_line) > lcd_length:
        print("too long first line")
    if len(secound_line) > lcd_length:
        print("too long secound line")
    lcd.clear()
    lcd.message(f"{first_line}\n{secound_line}")


def final_info(m_time, energy):
    m_time = str(m_time)[:5]
    energy = str(energy)[:5]
    lcd.clear()
    lcd.message(f"Test complited:\n{m_time}s {energy}mAh")


if __name__ == "__main__":
    measure_show(1234567890123456, 123456789, 123456789, 123456789)
    time.sleep(5)
    message("test first line",  "secound line")
    time.sleep(5)
    final_info(123456789, 123456789)
