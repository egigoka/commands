#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with keyboard
"""
__version__ = "0.2.0"


class Keyboard:

    @staticmethod
    def hotkey(*args, verbose=False, **kwargs):
        import pyautogui
        if verbose:
            print(f"Keyboard.hotkey({args=}, {kwargs=})")
        return pyautogui.hotkey(*args, **kwargs)

    # https://github.com/asweigart/pyautogui/issues/137

    @staticmethod
    def translate(key):
        """Returns qwerty key or the given key itself if no mapping found"""
        qwerty = "qwertyuiop[]asdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
        ycuken = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖ\ЭЯЧСМИТЬБЮ,"

        tr = dict(zip(ycuken, qwerty))  # join as keys and values

        return "".join(map(lambda x: tr.get(x), key))

    @classmethod
    def translate_string(cls, string):
        output = ""
        for symbol in string:
            output += cls.translate(symbol)
        return output

    @classmethod
    def write(cls, string, verbose=False):
        import pyautogui

        output = cls.translate_string(string)

        if verbose:
            print(f'Keyboard.write("{string}") -> pyautogui.write("{output}")')

        pyautogui.write(output)
