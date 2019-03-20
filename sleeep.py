import time
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


print("started slep")

cnt = 0
while cnt < 5:
    time.sleep(cnt+1)
    cnt += cnt + 1
    print(cnt)
    eprint(f"stderr {cnt}")
print("ended slep")
print("raising error")
raise Exception("yep")