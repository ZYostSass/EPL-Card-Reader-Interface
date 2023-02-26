import serial

PORT = "/dev/pts/3"
BAUD = 9600
BYTESIZE = serial.EIGHTBITS
TIMEOUT = 0
card_number = 1237836
fac_number = 65794


print(10)
binary_data = "0" + format(fac_number, "016b") + format(card_number << 1, "019b")
print(12)
hex_data = hex(int(binary_data, 2))[2:].upper()
print(14)
if len(hex_data) < 12:
    hex_data = ("0" * (12 - len(hex_data))) + hex_data
print(17)
# Add CRLF
output = hex_data + "\r\n"
print(20)
# Open serial port

try:
    ser = serial.Serial(port=PORT, baudrate=BAUD, bytesize=BYTESIZE, timeout=TIMEOUT)
except Exception as e:
    print("Error opening port: " + str(e))
print(26)  
# Send output to serial port
ser.write(output.encode())
print(29)


# Print output
print("Output sent to serial port: " + output)
