import threading
import time

def worker():
    print("Worker sleeping...")
    time.sleep(10)
    print("Worker done")

t = threading.Thread(target=worker)
t.start()

try:
    print("Main thread: waiting for worker")
    t.join()
except KeyboardInterrupt:
    print("Main thread: got Ctrl+C while waiting!")
