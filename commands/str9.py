#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing strings.
"""
__version__ = "0.14.0"


class Str:
    """Class with functions for managing strings.
    """
    @staticmethod
    def to_quotes(some_string):
        """
        <br>`param some_string` string
        <br>`return` string, inside "" quotes
        """
        return '"' + str(some_string) + '"'

    @staticmethod
    def to_quotes_2(some_string):
        """
        <br>`param some_string` string
        <br>`return` string, inside '' quotes
        """
        return "'" + str(some_string) + "'"

    @classmethod
    def get_integers(cls, string, float_support=True, debug=False):
        """
        <br>`param string` string, with some integers or floats inside
        <br>`param float_support` boolean, enable float support
        <br>`param debug` boolean, debug print enable
        <br>`return` list of integers or floats
        """
        string = cls.remove_spaces(string)
        integer_found = False
        integers = []
        current_integer = 0
        negative = False
        floatn = None
        for symbol in str(string) + " ":  # in exception some processing, meh :(
            try:
                if symbol in ['-', '—'] and not integer_found:
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
        <br>`param string` string, with some newlines
        <br>`param quiet` boolean suppress print to console
        <br>`return` list of strings
        """
        from .const9 import newline, newline2
        if isinstance(string, str):  # if input is string
            string = string.replace(newline2, newline)
            strings = string.split(newline)
            return strings
        else:
            raise TypeError(str(type(string)) + " can't be splitted")

    @classmethod
    def nl(cls, string):  # pylint: disable=invalid-name
        """
        <br>`param string` string, with some newlines
        <br>`param quiet` boolean suppress print to console
        <br>`return` list of strings
        """
        return cls.newlines_to_strings(string=string)

    @staticmethod
    def split_every(string, chars):
        """Split line every N chars
        <br>`param string` string, input
        <br>`param chars` int, count of chars, that split line
        <br>`return` list of substring of 'chars' length
        """
        chars = int(chars)
        if chars <= 0:
            raise ValueError("chars must be positive, not", chars)
        if not isinstance(string, (int, str)):
            raise ValueError("type", type(string), "isn't supported by Str.split_every")
        string = str(string)
        import re
        char_exists = "."
        char_can_be_exists = ".?"
        regexp = char_exists + char_can_be_exists*(chars-1)
        return re.findall(regexp, string, re.DOTALL)


    @staticmethod
    def leftpad(string, length, char="0", rightpad=False):
        """Adds symbols from char str to left side of output string to change input string len to 'length'
        <br>`param string` string, input
        <br>`param length` int, len of output string
        <br>`param char` string, characters, added to left side of input string
        <br>`param rightpad` boolean, if True, adds symbols to right side
        <br>`return` string, with added characters to side of input string
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
    def rightpad(cls, string, length, char="0"):
        """Adds symbols from char str to right side of output string to change input string len to 'length'
        <br>`param string` string, input
        <br>`param length` int, len of output string
        <br>`param char` string, characters, added to right side of input string
        <br>`return` string, with added characters to side of input string
        """
        return cls.leftpad(string, length, char=char, rightpad=True)

    @staticmethod
    def substring(string, before, after=None, return_after_substring=False, safe=False, exception_message=None):
        """Get substring from string that between "before", and "after" strings, not including those.
        <br>`param string` string
        <br>`param before` string, that before output string
        <br>`param after` string, that after output string
        <br>`param return_after_substring` boolean, if True, return list of substring and part after substring
        <br>`param safe` boolean, suppress exceptions if something not found
        <br>`param exception_message` string, will be in exception that raised
        <br>`return` string, from string that between "before", and "after" arguments
        """
        if isinstance(string, bytes):
            from .bytes9 import Bytes
            string = Bytes.to_string(string)
        if isinstance(before, bytes):
            from .bytes9 import Bytes
            before = Bytes.to_string(before)
        startfrom = string.find(before)
        if startfrom != -1:
            startfrom = string.find(before) + len(before)
        else:
            startfrom = 0
            if not safe:
                if isinstance(exception_message, str):
                    exception_message += '. '
                elif exception_message is None:
                    exception_message = ""
                raise KeyError(f"{exception_message}The line preceding ({before}) the search string was not found")
        if after:
            if isinstance(after, bytes):
                from .bytes9 import Bytes
                after = Bytes.to_string(after)
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
                    if isinstance(exception_message, str):
                        exception_message += '. '
                    elif exception_message is None:
                        exception_message = ""
                    raise KeyError(f"{exception_message}The string ({after}) that followed the search string was not found")
        else:
            substring = string[startfrom:]
        if return_after_substring:
            return substring, after_substring
        return substring

    @staticmethod
    def diff_simple(string_a, string_b):
        """Print all different symbols. Code not all mine, so it's not so good (or bad).
        <br>`param string_a` string
        <br>`param string_b` string
        <br>`return` None
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
        <br>`param string` string, with message to user, that asks password
        <br>`return` string, that returned from getpass lib
        """
        import getpass
        return getpass.getpass(str(string))

    @classmethod
    def input_int(cls, message="Input integer: ", minimum=None, maximum=None, default=None, debug=True):  # pylint: disable=too-many-arguments
        """Ask user to input integer.
        <br>`param message` string, message to user
        <br>`param minimum` minimum value of returned integer
        <br>`param maximum` maximum value of returned integer
        <br>`param default` default value if user just press Enter
        <br>`param debug` boolean, debug purposes
        <br>`return` int, input from user
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
        <br>`param string_` string, input
        <br>`return` string, without duplicated spaces
        """
        string_ = str(string_)
        while '  ' in string_:
            string_ = string_.replace('  ', ' ')
        return string_

    @staticmethod
    def get_words(string_):
        """
        <br>`param string_` string, with spaces to split it
        <br>`return` list of substrings, splitted by space|multiple space
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
        <br>`param seed` string, seed to generate guid
        <br>`return` string, guid-like
        """
        import hashlib
        bseed = bytes(seed, "utf-8")
        hash = hashlib.sha256(bseed)
        hashhex = hash.hexdigest()
        strhashhex = str(hashhex)
        symbols = strhashhex.zfill(32)[-32:]  # adds zeros if needed and cut unneded symbols
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string

    @staticmethod
    def encrypt(string, password):
        int_list = []
        password_len = len(password)
        for cnt, sym in enumerate(string):
            password_sym = password[cnt % password_len]
            int_list.append(ord(sym) - ord(password_sym))
        return int_list

    @staticmethod
    def decrypt(int_list, password):
        output_string = ""
        password_len = len(password)
        for cnt, numb in enumerate(int_list):
            password_sym = password[cnt % password_len]
            output_string += chr(numb + ord(password_sym))
        return output_string

    seeds = []

    @classmethod
    def guid_by_seed(cls, seed, uniq_in_process=True):
        if seed in cls.seeds:
            if uniq_in_process:
                raise KeyError(fr"seed '{seed}' already used by guid_by_seed")
        else:
            cls.seeds.append(seed)
        import hashlib
        bseed = bytes(seed, "utf-8")
        hash = hashlib.sha256(bseed)
        hashhex = hash.hexdigest()
        strhashhex = str(hashhex)
        symbols = strhashhex.zfill(32)[-32:]  # adds zeros if needed and cut unneded symbols
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string


    @staticmethod
    def rreplace(string: str, old: str, new: str, occurrence: int):
        '''Right replace. Replacing
        :param string: str, string, where to replace
        :param old: str, substring to replace
        :param new: str, substring to insert
        :param occurrence: int, count of replcacement from right
        :return: str, string with replaced substrings
        '''
        # https://stackoverflow.com/a/2556252/6519078
        if not isinstance(string, str):
            string = str(string)
        if not isinstance(old, str):
            old = str(old)
        if not isinstance(new, str):
            new = str(new)
        if not isinstance(occurrence, int):
            occurrence = int(occurrence)

        _list = string.rsplit(old, occurrence)
        return new.join(_list)

    @staticmethod
    def is_ascii(string):
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True


    python_encodings = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850',
                        'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865',
                        'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140',
                        'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258',
                        'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz',
                        'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3',
                        'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
                        'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14',
                        'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland',
                        'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004',
                        'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8']
