from time import sleep
from reader import CardReader

# Create an instance of the CardReader class
reader = CardReader()

try:
    while True:
        # Read data from the card reader
        data = reader.get_data()
        if data is not None:
            # Print the card number and facility code
            print("Card number:", data[0])
            print("Facility code:", data[1])

        # Wait for a short time before checking for more data
        sleep(0.1)

except KeyboardInterrupt:
    # If the user presses Ctrl-C, exit cleanly
    pass

finally:
    # Close the serial port before exiting
    reader.close()
