import glob
import sys
import threading
import time
import serial
import serial.tools.list_ports


def start_card_reader():
    card_reader_lock = threading.Lock()
    card_reader_thread = threading.Thread(
        target=make_card_loop,
        name="EPL Card Reader",
        daemon=True,
        args=card_reader_lock
    )
    card_reader_thread.start()
    return card_reader_lock

def make_card_loop(lock: threading.Lock):
    card_reader = CardReader()
    while True:
        data = card_reader.get_data()
        if data is not None:
            lock.acquire()
            print("GOT DATA")
            print(data)
        time.sleep(0.1)
        


class CardReader:
    # Constructor takes baud_rate and optionally a port path
    # Instead of relying on input for the port path, it now
    # locates the card reader by either a passed in device name
    # or the default value.
    def __init__(self, port=None, baud_rate=9600, device_name=None):
        print("HERE1")
        if port:
            print("HERE2")
            self.port = port
        else:
            print("HERE3")
            self.port = self.set_port(device_name)
        print("HERE4")
        self.baud_rate = baud_rate
        print("HERE5")
        self.ser = serial.Serial(
            port=self.port, baudrate=self.baud_rate, timeout=1)
        print("HERE6")

    def ports(self):
        result = []
        for p in serial.tools.list_ports.comports():
            result.append(p)
        return result

    # Uses the serial tools library to get a list of ports and
    # searches for the name of the reader.
    # If found, this is passed to the constructor and set
    # Otherwise raises an Exception - validate the port name in use
    def set_port(self, device_name=None):
        print("HERE7")
        if not device_name:
            print("HERE8")
            device_name = 'USB to UART'
        print("HERE9")
        ports = serial.tools.list_ports.comports()
        print("HERE10")
        for port in ports:
            print("HERE11")
            if device_name in port.name or device_name in port.description:
                print("HERE12")
                return port.device
        print("HERE13")
        for port in ports:
            print("HERE14")
            if '/dev/' in port.device or '/dev/' in port.name or '/dev/' in port.description:
                print("HERE15")
                return port.device
        raise Exception("No port found at " + device_name)

    # When called, checks for data in serial buffer. If present, it
    # formats the hexadecimal string (See card reader documentation)
    # and returns the card number and facility code as a tuple.
    # A None response indicates no data in buffer
    # TODO: add proper error handling
    def get_data(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode().strip()
            clean = data[4:]
            clean_int = int(clean, 16)
            # Bitshift to remove parity and mask to isolate 19 bits
            card_number = (clean_int >> 1) & 0x7FFFF
            facility_code = (clean_int >> 20)
            # print(f"Card: " + str(card_number))
            # print(f"Fac: " + str(facility_code))
            self.ser.reset_input_buffer()
            return (card_number, facility_code)
        else:
            return None
    # See documentation here: https://pyserial.readthedocs.io/en/latest/tools.html
    # Get a list of ports
    # port.device contains the full pathname of the port (eg '/dev/ttyUSB0')
    # Return a list of open port names.
    # May be removed later

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port in ports:
            print(port)
            port_list.append(port.device)
        print(port_list)
        return port_list

    def close(self):
        self.ser.close()
