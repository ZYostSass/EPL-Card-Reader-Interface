import serial
import time

class CardReader:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=1)
        

    def get_data(self):
      if self.ser.in_waiting > 0:
        data = self.ser.readline().decode().strip()
        clean = data[4:]
        clean_int = int(clean, 16)
        card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
        facility_code = (clean_int >> 20)
        print(f"Card: " + str(card_number))
        print(f"Fac: " + str(facility_code))
        self.ser.reset_input_buffer()
        return (card_number, facility_code)
      else:
        return None

    def close(self):
      self.ser.close()

