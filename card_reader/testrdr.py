from reader import CardReader
import multiprocessing

def start_card_reader():
    reader = CardReader()
    try:
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

if __name__ == "__main__":
    card_reader_process = multiprocessing.Process(target=start_card_reader)
    card_reader_process.start()
