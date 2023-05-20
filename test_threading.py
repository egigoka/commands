from commands import *

def run(number):
    while True:
        print(f"{number} running")
        Time.sleep(10)

def count(tt):
    while True:
        cnt = tt.running_threads()
        Print.colored(f"{cnt} threads running", "magenta")
        Time.sleep(10)

tt = Threading(max_threads=11, verbose=True, start_from_first=True)
for i in Int.from_to(1,10):
    tt.add(run, args=(i,))
tt.add(count, args=(tt,))
tt.start(wait_for_keyboard_interrupt=True) 
