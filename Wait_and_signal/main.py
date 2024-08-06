import threading
import time

# Shared boolean variable representing whether Critical Section are in use
Critical_Section_in_use = False

# Condition variable for synchronization
condition = threading.Condition()

# Function representing a process
def process_func(process_id):
    global Critical_Section_in_use
    with condition:
        while Critical_Section_in_use:
            condition.wait()  # Wait until Critical Section are available
        Critical_Section_in_use = True  # Critical Section are now in use
        print(f"Process {process_id} is trying to enter the Critical Section..")
        print(f"Process {process_id} has entered the Critical Section and is running...")
        # Simulate some work
        time.sleep(3)
        print(f"Process {process_id} has finished and Exited the Critical Section.")
        Critical_Section_in_use = False  # Release the Critical Section
        condition.notify()  # Notify waiting threads

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
print("&& All processes have finished execution &&")