import flask
import flask_socketio
import serial
import time
import datetime
import json
import multiprocessing


class CardReaderProcess(multiprocessing.Process):

    def __init__(self, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
        super().__init__()

        self.app = app
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

    def run(self):
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