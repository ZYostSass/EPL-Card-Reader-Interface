import serial
import threading

print("Testing card reader in single thread...")

try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
    while True:
        try:
            data = ser.readline().decode().strip()
            if not data:
                print("No data read!")
                continue
            if data:
                clean = data[:2]
                clean_int = int(clean, 16)
                card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
                facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
                print(f"Card number: {card_number}") # Verified when tested with my badge
                print(f"Facility Code: {facility_code}") 
                print("Card reader loop will now exit and close port for the single thread test.")
                ser.close()
                break
        except Exception as e:
            print(f"Error reading data from serial port: {str(e)}")
            continue
except Exception as e:
            print("Error opening port: " + str(e))

