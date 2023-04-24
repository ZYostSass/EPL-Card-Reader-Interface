import serial
import threading
import traceback
import time

class CardReader:
    def __init__(self, port, baud_rate, callback):
        self.port = port
        self.baud_rate = baud_rate
        self.ser_lock = threading.Lock()
        self.ser = None
        self.callback = callback

    def read_serial(self):
        print("read_serial started!")
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baud_rate, timeout=1)
            # self.ser.reset_input_buffer()
            while True:
                try:
                    if self.ser.in_waiting > 0:
                        data = self.ser.readline().decode().strip()
                        if len(data) > 0:
                            print(f"Data sent to main thread: {data}")
                            self.callback(data) # Return data to main thread
                            continue
                        else:
                            continue
                        # self.ser.reset_output_buffer()
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    print(f"Error reading data from serial port: {str(e)}")
                    traceback.print_exc()
                    continue

        except Exception as e:
            print("Error opening port: " + str(e))
            traceback.print_exc()
        finally:
            if self.ser:
                self.ser.close()
