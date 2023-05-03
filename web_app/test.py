import serial

PORT = "/dev/pts/2"
BAUD = 9600
BYTESIZE = serial.EIGHTBITS
TIMEOUT = 0
hex_value = b'25101025C698\r\n'




try:
    ser = serial.Serial(port=PORT, baudrate=BAUD, bytesize=BYTESIZE, timeout=TIMEOUT)
except Exception as e:
    print("Error opening port: " + str(e))
print(26)
# Send output to serial port
ser.write(hex_value)
print(29)


# Print output
print("Output sent to serial port: ",hex_value)
