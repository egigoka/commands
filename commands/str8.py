#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing strings.
"""
__version__ = "0.11.0"


class Str:
    """Class with functions for managing strings.
    """
    @staticmethod
    def to_quotes(some_string):
        """
        :param some_string: string
        :return: string, inside "" quotes
        """
        return '"' + str(some_string) + '"'

    @staticmethod
    def to_quotes_2(some_string):
        """
        :param some_string: string
        :return: string, inside '' quotes
        """
        return "'" + str(some_string) + "'"

    @classmethod
    def get_integers(cls, string, float_support=True, debug=False):
        """
        :param string: string, with some integers or floats inside
        :param float_support: boolean, enable float support
        :param debug: boolean, debug print enable
        :return: list of integers or floats
        """
        string = cls.remove_spaces(string)
        integer_found = False
        integers = []
        current_integer = 0
        negative = False
        floatn = None
        for symbol in str(string) + " ":  # in exception some processing, meh :(
            try:
                if symbol in ['-', '—']:
                    negative = True
                    continue
                if float_support:
                    if symbol in [".", ","]:
                        if isinstance(floatn, int):
                            floatn = None
                            raise ValueError  # goto to except block code
                        floatn = 0
                        continue
                int(symbol)
                if isinstance(floatn, int):
                    floatn += 1
                    value_before = current_integer
                    added_value = int(symbol)*pow(10, -floatn)
                    current_integer = current_integer + added_value
                    if debug:
                        print("value_before", value_before, "floatn", floatn, "added_value", added_value,
                              "current_integer", current_integer)
                    current_integer = round(current_integer, floatn)  # to reduce problems with floating numbers
                else:
                    current_integer = current_integer*10 + int(symbol)
                integer_found = True
            except ValueError:
                if integer_found:
                    if negative:
                        current_integer = -current_integer
                    integers = integers + [current_integer]
                    current_integer = 0
                    integer_found = False
                negative = False
                floatn = None
        return integers

    @staticmethod
    def newlines_to_strings(string):
        """
        :param string: string, with some newlines
        :param quiet: boolean suppress print to console
        :return: list of strings
        """
        from .const8 import newline, newline2
        if isinstance(string, str):  # if input is string
            string = string.replace(newline2, newline)
            strings = string.split(newline)
            return strings
        else:
            raise TypeError(str(type(string)) + " can't be splitted")

    @classmethod
    def nl(cls, string):  # pylint: disable=invalid-name
        """
        :param string: string, with some newlines
        :param quiet: boolean suppress print to console
        :return: list of strings
        """
        return cls.newlines_to_strings(string=string)

    @staticmethod
    def split_every(string, chars):
        """Split line every N chars
        :param string: string, input
        :param chars: int, count of chars, that split line
        :return: list of substring of 'chars' length
        """
        chars = int(chars)
        if chars <= 0:
            raise ValueError("chars must be positive, not", chars)
        if not isinstance(string, (int, str)):
            raise ValueError("type", type(string), "isn't supported by Str.split_every")
        string = str(string)
        import re
        output_lines = []
        char_exists = "."
        char_can_be_exists = ".?"
        regexp = char_exists + char_can_be_exists*(chars-1)
        for line in re.findall(regexp, string):  # todo can I just return this list?
            output_lines += [line]
        return output_lines

    @staticmethod
    def leftpad(string, length, char="0", rightpad=False):
        """Adds symbols from char str to left side of output string to change input string len to 'length'
        :param string: string, input
        :param length: int, len of output string
        :param char: string, characters, added to left side of input string
        :param rightpad: boolean, if True, adds symbols to right side
        :return: string, with added characters to side of input string
        """
        char = str(char)
        string = str(string)
        if len(string) >= length:
            return string
        str_of_chars = str(char) * int((length/len(char))+1)
        string_output = str_of_chars[len(string):length] + string
        if rightpad:
            string_output = string + str_of_chars[len(string):length]
        return string_output

    @classmethod
    def rightpad(cls, string, leng, char="0"):
        """Adds symbols from char str to right side of output string to change input string len to 'length'
        :param string: string, input
        :param length: int, len of output string
        :param char: string, characters, added to right side of input string
        :return: string, with added characters to side of input string
        """
        return cls.leftpad(string, leng, char=char, rightpad=True)

    @staticmethod
    def substring(string, before, after=None, return_after_substring=False, safe=False):
        """Get substring from string that between "before", and "after" strings, not including those.
        :param string: string
        :param before: string, that before output string
        :param after: string, that after output string
        :param return_after_substring: boolean, if True, return list of substring and part after substring
        :param safe: boolean, suppress exceptions if something not found
        :return: string, from string that between "before", and "after" arguments
        """
        string = str(string)
        before = str(before)
        startfrom = string.find(before)
        if startfrom != -1:
            startfrom = string.find(before) + len(before)
        else:
            startfrom = 0
            if not safe:
                raise KeyError("The line preceding ({}) the search string was not found".format(before))
        if after:
            after = str(after)
            end_at = string[startfrom:].find(after)
            if end_at != -1:
                end_at += startfrom
                substring = string[startfrom:end_at]
                if return_after_substring:
                    after_substring = string[end_at:]
            else:
                substring = string[startfrom:]
                if return_after_substring:
                    after_substring = ""
                if not safe:
                    raise KeyError("The string ({}) that followed the search string was not found".format(after))
        else:
            substring = string[startfrom:]
        if return_after_substring:
            return substring, after_substring
        return substring

    @staticmethod
    def diff_simple(string_a, string_b):
        """Print all different symbols. Code not all mine, so it's not so good (or bad).
        :param string_a: string
        :param string_b: string
        :return: None
        """
        import difflib
        strings = [(string_a, string_b)]  # for furthurer support for unlimited srtings
        for symbol_a, symbol_b in strings:
            print('{} => {}'.format(symbol_a, symbol_b))
            for i, symbol in enumerate(difflib.ndiff(symbol_a, symbol_b)):
                if symbol[0] == ' ':
                    continue
                elif symbol[0] == '-':
                    print(u'Delete "{}" from position {}'.format(symbol[-1], i))
                elif symbol[0] == '+':
                    print(u'Add "{}" to position {}'.format(symbol[-1], i))
            print()

    @staticmethod
    def input_pass(string="Password:"):
        """Secure input password
        :param string: string, with message to user, that asks password
        :return: string, that returned from getpass lib
        """
        import getpass
        return getpass.getpass(str(string))

    @classmethod
    def input_int(cls, message="Input integer: ", minimum=None, maximum=None, default=None, debug=True):  # pylint: disable=too-many-arguments
        """Ask user to input integer.
        :param message: string, message to user
        :param minimum: minimum value of returned integer
        :param maximum: maximum value of returned integer
        :param default: default value if user just press Enter
        :param debug: boolean, debug purposes
        :return: int, input from user
        """
        output_int = "jabla fitta"
        if default:
            message += "(Enter = " + str(default) + ") "
        while output_int == "jabla fitta":  # цикл, пока не получит итоговое число
            integer = input(message)
            if integer != "":
                try:
                    integer = cls.get_integers(integer)[0]
                except IndexError:
                    print("Это не число")
                    continue
            elif default and integer == "":
                output_int = default
                break
            elif integer == "":
                print("Это не число")
                raise ValueError
            if minimum:
                if int < minimum:
                    print("Число должно быть больше", minimum)
                    raise ValueError
            if maximum:
                if int > maximum:
                    print("Число должно быть меньше", maximum)
                    raise ValueError
            output_int = integer
            break
        if debug:
            print("Итоговое число:", output_int)
        return output_int


    @classmethod
    def remove_spaces(cls, string_):
        """Remove all duplicating spaces in string
        :param string_: string, input
        :return: string, without duplicated spaces
        """
        string_ = str(string_)
        while '  ' in string_:
            string_ = string_.replace('  ', ' ')
        return string_

    @staticmethod
    def get_words(string_):
        """
        :param string_: string, with spaces to split it
        :return: list of substrings, splitted by space|multiple space
        """
        removed_spaces = ' '.join(string_.split())  # at least, it's fast https://stackoverflow.com/questions/2077897/
        # substitute-multiple-whitespace-with-single-whitespace-in-python
        words = removed_spaces.split(" ")
        if words == [""]:
            words = []
        return words

    @staticmethod
    def guid_from_seed(seed):
        """
        :param seed: string, seed to generate guid
        :return: string, guid-like
        """
        import hashlib
        bseed = bytes(seed, "utf-8")
        hash = hashlib.sha256(bseed)
        hashhex = hash.hexdigest()
        strhashhex = str(hashhex)
        symbols = strhashhex.zfill(32)[-32:]  # adds zeros if needed and cut unneded symbols
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string