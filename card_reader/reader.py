import serial, serial.tools.list_ports
import multiprocessing
import time
import json


# Driver for Windows installed from here: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads
class CardReader:
    # Constructor takes baud_rate and optionally a port path
    # Instead of relying on input for the port path, it now 
    # locates the card reader by either a passed in device name
    # or the default value.
    _lock = Lock()
    def __init__(self, device_name=None, port=None, serial_port=None):
     
      try:
        if port:
          self.port = port
        else:
          self.port = self.set_port(device_name)
        if serial_port:
           self.ser = serial_port
        else:
          self.baudrate = 9600
          self.bytesize = serial.EIGHTBITS
          self.parity = serial.PARITY_NONE
          self.stopbits = serial.STOPBITS_ONE
          self.timeout = 1
          
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

      
    # When called, checks for data in serial buffer. If present, it 
    # formats the hexadecimal string (See card reader documentation)
    # and returns the card number and facility code as a tuple.
    # A None response indicates no data in buffer
    # TODO: add proper error handling
    def get_data(self):
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
                time.sleep(2)
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

                # Save the data to a file
                with open('card_data.json', 'w') as f:
                    json.dump({
                        'card_number': card_number,
                        'facility_code': facility_code
                    }, f)
                time.sleep(1)
        except Exception as e:
            print(f"An error occurred while reading badge data: {e}")
        finally:
            self.ser.close()
            self._lock.release()

        return (card_number, facility_code) if card_number and facility_code else None

    def start_reading_loop(self):
        def read_loop(card_reader):
            while True:
                card_reader.get_data()
                time.sleep(1)

        self.read_process = multiprocessing.Process(target=read_loop, args=(self,))
        self.read_process.start()   

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
    
    def read_loop(self):
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
      self.ser.close()

