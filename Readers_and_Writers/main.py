from threading import Thread, Semaphore
import time

class ReadersWriters:
    def __init__(self):
        self.readers_count = 0
        self.resource = 0
        self.mutex = Semaphore(1)  # For mutual exclusion
        self.reader_sem = Semaphore(1)  # For controlling access to readers_count
        self.writer_sem = Semaphore(1)  # For controlling access to resource

    def reader(self, reader_id):
        while True:
            time.sleep(1)  # Simulating reading
            self.reader_sem.acquire()
            self.readers_count += 1
            if self.readers_count == 1:
                self.writer_sem.acquire()  # Prevent writers while readers are present
            self.reader_sem.release()

            print(f"Reader {reader_id} is reading. Resource value: {self.resource}")

            self.reader_sem.acquire()
            self.readers_count -= 1
            if self.readers_count == 0:
                self.writer_sem.release()  # Allow writers if no readers
            self.reader_sem.release()

    def writer(self, writer_id):
        while True:
            time.sleep(2)  # Simulating writing
            self.writer_sem.acquire()  # Only one writer can access the resource
            self.mutex.acquire()  # Ensure mutual exclusion
            self.resource += 1
            print(f"Writer {writer_id} is writing. New resource value: {self.resource}")
            self.mutex.release()
            self.writer_sem.release()

if __name__ == "__main__":
    rw = ReadersWriters()

    # Creating reader threads
    for i in range(3):
        reader_thread = Thread(target=rw.reader, args=(i,))
        reader_thread.start()

    # Creating writer threads
    for i in range(2):
        writer_thread = Thread(target=rw.writer, args=(i,))
        writer_thread.start()
