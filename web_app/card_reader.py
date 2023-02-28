import serial
import sys

PORT = "/dev/pts/3"

BAUD = 9600
BYTESIZE = serial.EIGHTBITS
TIMEOUT = 0

raw_input = b''

# Connect to port

    
# Main loop - execute continuously to listen at the port - This works  
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
    
    # While the transfer of data works as expected, conversion and formatting does not
    # Currently using socat to simulate serial ports inside a vbox - have ordered a reader from provided docs
    print(raw_input)
    raw_data = int.from_bytes(raw_input.rstrip(), byteorder=sys.byteorder) # Remove trailing whitespace (CRLF)
    print(raw_data)
    card_number = (raw_data >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
    facility_code = (raw_data >> 20)  & 0xFFFF # Same for facility code

    # Convert card number and facility code to ASCII
    card_number_ascii = str(card_number)
    facility_code_ascii = str(facility_code)

    # Output to console and file for now
    
    if len(card_number_ascii) > 0 and len(facility_code_ascii) > 0:
        print("Card Number (ASCII): " + card_number_ascii)
        print("Facility Code (ASCII): " + facility_code_ascii)
        with open("rdr_output.txt", "a") as file:
            file.write("Card Number (ASCII): " + card_number_ascii)
            file.write("Facility Code (ASCII):  " + facility_code_ascii)
    
   
    
        
    # After writing to file, reset everything
    ser.flushInput()
    raw_input = b''
    raw_data = 0
    card_number = ''
    facility_code = ''
    card_number_ascii = ''
    facility_code_ascii = ''
    ser.close()
    
