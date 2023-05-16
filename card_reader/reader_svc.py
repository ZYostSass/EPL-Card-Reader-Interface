import serial, serial.tools.list_ports
import time, datetime
import json
from flask_socketio import emit, join_room
from flask import request
import multiprocessing

class CardReader:
  def __init__(self, app, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
      try:
          if port:
              self.port = port
          else:
              self.port = self.set_port()
          self.baudrate = baudrate
          self.bytesize = bytesize
          self.parity = parity
          self.stopbits = stopbits
          self.timeout = timeout
          self.file_path = 'card_data.json'
          self.file = open(self.file_path, 'a') 
          self.ser = None 
          self.open_port()
          self.socketio = None

      except Exception as e:
          print(f"An error occurred while initializing the card reader: {e}")

  def run(self):
      try:
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout
        )
        while True:
            data = self.ser.readline().decode()
            if data:
                clean = data[4:]
                if clean:
                    clean_int = int(clean, 16)
                    card_number = (clean_int >> 1) & 0x7FFFF
                    facility_code = (clean_int >> 20)

                    self.app.socketio.emit('card_data', {
                        'card_number': card_number,
                        'facility_code': facility_code
                    }, namespace='/card_reader')
      except Exception as e:
          print(f"An error occurred while running the card reader: {e}")

  # Uses the serial tools library to get a list of ports and 
  # searches for the name of the reader.
  # If found, this is passed to the constructor and set
  # Otherwise raises an Exception - validate the port name in use
  # Takes an optional string parameter to search for a specific device name
  def set_port(self, device_name=None):
    if not device_name:
        device_name = 'USB to UART Bridge'
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print("Name: " + port.name + "  " + "Desc: " + port.description + "Device: " + port.device)
        if device_name in port.name or device_name in port.description:
            return port.device
    raise Exception("No port found with the device name: " + port.device)
  
  def set_socketio(self, socketio):
      self.socketio = socketio

  def emit_card_data(self, card_num, fac_code):
      card_data = {
          'card_number': card_num,
          'facility_code': fac_code
      }
      if self.socketio is not None:
          self.socketio.emit('card_data', card_data, namespace='/card_reader')

  # Extracted the port opening to a separate method
  def open_port(self):
      print("Opening port:", self.port)
      try:
          self.ser = serial.Serial(
              port=self.port,
              baudrate=self.baudrate,
              bytesize=self.bytesize,
              parity=self.parity,
              stopbits=self.stopbits,
              timeout=self.timeout
          )
          print("Serial port opened:", self.ser)
      except Exception as e:
          print(f"An error occurred while opening the serial port: {e}")

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
  
  def get_data(self):
          card_number = None
          facility_code = None
          try:
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
                  self.emit_card_data(card_number, facility_code)
              return card_number, facility_code
          except Exception as e:
              print(f"An error occurred while reading badge data: {e}")

  def read_loop(self):
    while True:
      print("read_loop executing!")
      self.get_data()
      time.sleep(2)

  def start_reading_loop(self):
      print("Starting reading loop")
      try:
          self.read_process = multiprocessing.Process(target=self.read_loop)
          self.read_process.start()
      except Exception as e:
          print(f"An error occurred while starting the reading loop process: {e}")

if __name__ == '__main__':
    from flask import jsonify

    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/card_data')
    def card_data():
        return jsonify({
            'card_number': '1234567890',
            'facility_code': '123'
        })

    socketio = flask_socketio.SocketIO(app)

    reader_process = CardReaderProcess(app, '/dev/ttyUSB0', 9600, 8, 'N', 1)
    reader_process.start()

    app.run(debug=True)