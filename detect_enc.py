from commands import *
a = Console.get_output("echo ФЫВА", pureshell=True, timeout=1, auto_decoding=False)
print(repr(a))
print(a)
for enc in File.all_encodings:
    try:
        print(enc)
        print(a.decode(enc))
    except Exception as e:
        print(e)