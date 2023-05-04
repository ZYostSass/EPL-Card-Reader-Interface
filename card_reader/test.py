import serial
import time
from reader import CardReader

def main():
    port = "/dev/ttyUSB0"
    print("Using port:", port)

    card_reader = CardReader(baud_rate=9600)
    for i in range(10):
        card_data = card_reader.get_data()
        if card_data:
            print("Card data:", card_data)
        time.sleep(1)
    
    card_reader.get_ports()
    card_reader.close()

if __name__ == "__main__":
    main()
