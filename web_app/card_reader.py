import serial
import time

PORT = "/dev/pts/4"
BAUD = 9600
BYTESIZE = serial.EIGHTBITS
TIMEOUT = 0

raw_input = b''

# Connect to port

    
# Main loop - execute continuously to listen at the port    
while True:
    try:
        ser = serial.Serial(port=PORT, baudrate=BAUD, bytesize=BYTESIZE, timeout=TIMEOUT)
    except Exception as e:
        print("Error opening port: " + str(e))
        
    while True: 
        next_byte = ser.read(1)
        raw_input += next_byte
        if len(raw_input) >= 14:
            break
    

    print(raw_input)
    raw_data = int(raw_input[:12], 16)
    print(raw_data)
    card_number = (raw_data >> 1) # & 0x7FFFF
    facility_code = (raw_data >> 20) # & 0xFFFF

    # Convert card number and facility code to ASCII
    card_number_ascii = str(card_number)
    facility_code_ascii = str(facility_code)

    # Print ASCII representation
    print("Card Number (ASCII): " + card_number_ascii)
    print("Facility Code (ASCII): " + facility_code_ascii)
    
    with open("rdr_output.txt", "a") as file:
        file.write("Card Number (ASCII): " + card_number_ascii)
        file.write("Facility Code (ASCII):  " + facility_code_ascii)
    ser.flushInput()
    ser.close()
    
