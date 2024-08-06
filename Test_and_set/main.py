import threading
import time

# Shared boolean variable representing the lock
lock = threading.Lock()

# Counter to track the number of finished processes
finished_processes = 0

# Function representing a process
def process_func(process_id):
    global finished_processes
    print(f"Process {process_id} is trying to enter the Critical Section..")
    print(f"Process {process_id} is wating to enter the Critical Section....")
    with lock:
        print(f"Process {process_id} has entered the Critical Section and is running.")
        # Simulate some work
        time.sleep(3)
        print(f"Process {process_id} has finished and Exited the Critical Section.")
        finished_processes += 1

# Create and start processes
processes = []
for i in range(0, 5):
    process = threading.Thread(target=process_func, args=(i,))
    processes.append(process)
    process.start()

# Wait for all processes to finish
for process in processes:
    process.join()

# End threading after all processes are finished
print("$$ All processes have finished execution $$")