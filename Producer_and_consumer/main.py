import threading
import time
import random

BUFFER_SIZE = 5  # Size of the buffer
buffer = []      # Shared buffer
mutex = threading.Semaphore(1)  # Mutex semaphore to protect buffer access
empty = threading.Semaphore(BUFFER_SIZE)  # Semaphore to track empty slots
full = threading.Semaphore(0)   # Semaphore to track filled slots

def producer():
    while True:
        item = random.randint(1, 100)
        empty.acquire()  # Wait for an empty slot
        mutex.acquire()  # Lock the buffer
        buffer.append(item)
        print(f"Produced {item}, buffer: {buffer}")
        mutex.release()  # Unlock the buffer
        full.release()   # Signal that buffer is no longer empty
        time.sleep(random.uniform(0.1, 0.5))  # Simulate production time

def consumer():
    while True:
        full.acquire()   # Wait for a filled slot
        mutex.acquire()  # Lock the buffer
        item = buffer.pop(0)
        print(f"Consumed {item}, buffer: {buffer}")
        mutex.release()  # Unlock the buffer
        empty.release()  # Signal that buffer is no longer full
        time.sleep(random.uniform(0.1, 0.5))  # Simulate consumption time

# Create producer and consumer threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for the threads to finish (which they won't in this example)
producer_thread.join()
consumer_thread.join()