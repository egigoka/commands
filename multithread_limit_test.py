from commands import *


def th(name):
    for i in Int.from_to(1,10):
        Time.sleep(1)


tt = Threading(verbose=True, max_threads=10, start_from_first=True)

for i in Int.from_to(1,100):
    tt.add(th, name=i, args=(i,))

b = Bench(verbose=True)
tt.start(wait_for_keyboard_interrupt=True)
b.end()
