import serial, serial.tools.list_ports
import time




def main():
    # Configure the serial port

    ser = serial.Serial(
        port="COM3",
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    
    

    # Check if the serial port is open
    if ser.is_open:
        print("Serial port is open.")
    else:
        print("Error: Serial port is not open.")
        return

    # Read and print data from the serial port
    try:
        while True:
            data = ser.readline().decode('utf-8').rstrip()
            if data:
                print("Received data: ", data)
            time.sleep(0.5)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Exiting...")

    # Close the serial port
    ser.close()

if __name__ == "__main__":
    main()
