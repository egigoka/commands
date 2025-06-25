import time
import traceback

_original_sleep = time.sleep

from commands import *
lock = Lock()

def traced_sleep(seconds):
#    with lock:
    print(f"\n⚠️ time.sleep({seconds}) called!")
    traceback.print_stack(limit=10)
    _original_sleep(seconds)

time.sleep = traced_sleep
