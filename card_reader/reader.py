import serial, serial.tools.list_ports
import multiprocessing
import time, datetime
import json


# This loop is supposed to execute in a sub-process while the main Flask app runs in the foreground
# Problem currently appears to be that the start_reading_loop() method is not being called when the 
# app is started. 
def read_loop(port=None, baudrate=None, bytesize=None, parity=None, stopbits=None, timeout=None):
    card_reader = CardReader(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout)
    while True:
        print("read_loop executing!")
        card_reader.get_data()
        time.sleep(2)
  
# Driver for Windows installed from here: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads
class CardReader:
    # Constructor takes baud_rate and optionally a port path
    # Instead of relying on input for the port path, it now 
    # locates the card reader by either a passed in device name
    # or the default value. 
    # The serial object is no longer called here - this was the issue with the 'Access Denied' error
    # Instead, the serial object is created in the get_data() method and closed after each read
    # This avoids the issue of the serial port being tied up by a different process
    # Stupid Windows grumble grumble
    
    _lock = multiprocessing.Lock() # Lock to prevent multiple processes from accessing the serial port at the same time
    def __init__(self, device_name=None, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
      try:
        if port:
          print("Port passed in: " + port)
          self.port = port
        else:
          self.port = self.set_port(device_name)

        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.file_path = 'card_data.json'
        self.file = open(self.file_path, 'a')  
      except Exception as e:
         print(f"An error occurred while initializing the card reader: {e}") # Fails here
     

    # Uses the serial tools library to get a list of ports and 
    # searches for the name of the reader.
    # If found, this is passed to the constructor and set
    # Otherwise raises an Exception - validate the port name in use
    def set_port(self, device_name=None):
      if not device_name:
          device_name = 'USB to UART Bridge'
      ports = serial.tools.list_ports.comports()
      for port in ports:
          print("Name: " + port.name + "  " + "Desc: " + port.description + "Device: " + port.device)
          if device_name in port.name or device_name in port.description:
              return port.device
      raise Exception("No port found with the device name: " + port.device)

    def write_to_file(self, data):
      try:
        print("Opening file:", self.file_path)
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        if len(lines) > 1000:
            with open(self.file_path, 'w') as f:
                f.writelines(lines[-1000:])
      except Exception as e:
          print(f"An error occurred while writing to file: {e}")
  
    # This method is called by the read_loop() method
    # When called it attempts to acquire a lock, open the serial port, read the data, and write it to a file.
    # This avoids the issue of the serial port being tied up by a different process
    # but there are some timing issues with the cardreader and physically swiping the badge.

    def get_data(self):
      print("get_data called")
      self._lock.acquire()
      card_number = None
      facility_code = None
      try:
          with serial.Serial(
                  port=self.port,
                  baudrate=self.baudrate,
                  bytesize=self.bytesize,
                  parity=self.parity,
                  stopbits=self.stopbits,
                  timeout=self.timeout
              ) as self.ser:
              time.sleep(1)
              print("Waiting: " + str(self.ser.in_waiting))
              if self.ser.in_waiting > 0:
                  data = self.ser.readline().decode()
                  clean = data[4:]
                  if clean:
                      clean_int = int(clean, 16)
                      card_number = (clean_int >> 1) & 0x7FFFF 
                      facility_code = (clean_int >> 20)
                  while self.ser.in_waiting:
                      self.ser.readline()
                  self.ser.reset_input_buffer()
                  self.write_to_file({
                      'timestamp': datetime.datetime.now().isoformat(),
                      'card_number': card_number,
                      'facility_code': facility_code
                  })
              time.sleep(1)
      except Exception as e:
          print(f"An error occurred while reading badge data: {e}")
      finally:
          self._lock.release()
    # Theoretically, this method launches a subprocess that executes the read_loop() method.
    # Works in the test script, but not in the FLask app.  Appears to be that the function call
    # is never executed.  Blocking?
    def start_reading_loop(self):
      print("Starting reading loop")
      try:
        self.read_process = multiprocessing.Process(target=self.read_loop)
        self.read_process.start()
      except Exception as e:
        print(f"An error occurred while starting the reading loop process: {e}")

    # See documentation here: https://pyserial.readthedocs.io/en/latest/tools.html
    # Get a list of ports 
    # port.device contains the full pathname of the port (eg '/dev/ttyUSB0')
    # Return a list of open port names.
    # May be removed later
    def get_ports(self):
      try:
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port in ports:
          print(port)
          port_list.append(port.device)
        print(port_list)
        return port_list
      except Exception as e:
         print(f"An error occurred while getting available serial ports: {e}")
         return []
   
    # Reads cards in loop and adds each item to list
    # Returns list on KeyboardInterrupt
    # Can change this to a button on the Flask app
    
    def looper(self):
      students = []
      try:
        while True:
          data = self.get_data()
          print(f"Data: {data}")
          if data is not None: # Not correctly filtering empty reader data
            students.append(data)
      except KeyboardInterrupt:
          return students
      except Exception as e:
         print(f"An error occurred while getting the list of students: {e}")
       
    def close(self):
      self.file.close()

if __name__ == "__main__":
    card_reader = CardReader()
    card_reader.start_reading_loop()