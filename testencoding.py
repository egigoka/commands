# -*- coding: utf-8 -*-
from commands import *
output, err = Console.get_output("echo ЕБАТЬ!", pureshell=True, return_merged=False, timeout=2, decoding=False, print_std=True, auto_decoding=False)
for enc in File.all_encodings:
    try:
        line = output.decode(enc)[:-1]
        print(enc)
        print(line)
        for sym in line:
            print(ord(sym))
    except Exception as e:
        print(e)