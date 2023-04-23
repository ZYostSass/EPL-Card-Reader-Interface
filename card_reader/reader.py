import serial
import threading

class CardReader:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser_lock = threading.Lock()
        self.ser = None

    def read_serial(self):
        print("read_serial started!")
        try:
            test_ct = 0
            self.ser = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=1)
            while True:
                try:
                    with self.ser_lock:
                        print("Locked!")
                        data = self.ser.readline().decode().strip()
                    if not data:
                        print("No data read!")
                        test_ct += 1 # Added this to verify loop is actually executing each turn
                        print(test_ct)
                        continue
                    clean = data[2:]
                    clean_int = int(clean, 16)
                    card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
                    facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
                   # print(card_number) # Verified when tested with my badge
                   # print(facility_code) # Not verified - No idea what my facility code should be
                except Exception as e:
                    print(f"Error reading data from serial port: {str(e)}")
                    continue

        except Exception as e:
            print("Error opening port: " + str(e))
        finally:
            if self.ser:
                self.ser.close()
