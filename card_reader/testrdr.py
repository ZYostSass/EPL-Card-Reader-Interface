from time import sleep
from reader import CardReader

# Create an instance of the CardReader class
reader = CardReader()

try:
    print("Reading cards. Press Ctrl-C to stop.")
    students = reader.read_loop()

except KeyboardInterrupt:
    # If the user presses Ctrl-C, exit cleanly
    print("Stopped reading cards.")

finally:
    # Print the card number and facility code for each student
    for student in students:
        print("Card #:", student[0])
        print("Facility #:", student[1])

    # Close the serial port before exiting
    reader.close()
