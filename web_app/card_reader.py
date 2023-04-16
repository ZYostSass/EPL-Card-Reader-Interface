import serial
import sys

PORT = "/dev/ttyUSB0"

BAUD = 9600
BYTESIZE = serial.EIGHTBITS
TIMEOUT = 0


# Connect to port

    
# Main loop - execute continuously to listen at the port - This works  
while True:
    try:
        ser = serial.Serial(port=PORT, baudrate=BAUD)
    except Exception as e:
        print("Error opening port: " + str(e))
        
    while True: 
        data = ser.readline().decode().strip()
        clean = data[2:]
        clean_int = int(clean, 16)
        print(clean_int)
        card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
        facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
        print(card_number)
        print(facility_code)
    
    
        
   
    
