from commands import *


def r(*args):
    return args


cf = CachedFunction(r, 3, quiet=False)

print(cf(1), 0, "run, update")

print(cf(1), 1, "run, no update")

print(cf(1), 2, "run, no update")

print(cf(1), 3, "run, update")

print(cf(1), 4, "run, no update")

print(cf(1), 5, "run, no update")
print(cf(1), 6, "run, update")
print(cf(1), 7, "run, no update")
print(cf(1), 8, "run, no update")
print(cf(1), 9, "run, no update")
print(cf(1), 10, "run, no update")
print(cf(1), 11, "run, no update")
print(cf(1), 12, "run, update")