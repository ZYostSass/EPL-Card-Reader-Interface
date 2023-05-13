from reader import CardReader

try:
    reader = CardReader()
    while True:
        data = reader.get_data()
        if data:
            print(f"Card number: {data[0]}, Facility code: {data[1]}")
except KeyboardInterrupt:
    print("\nInterrupted by user. Closing the reader.")
    reader.close()
except Exception as e:
    print(f"An error occurred: {e}")
    reader.close()
