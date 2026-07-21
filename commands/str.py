#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions for managing strings."""
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import difflib
    import getpass
    import hashlib
    import re
    from typing import Any, List, Optional, Tuple, Union
    from .bytes import Bytes
from .module import LazyModule, LazyProperty
__version__ = "0.15.1"
if not TYPE_CHECKING:
    re = LazyModule("re")
    difflib = LazyModule("difflib")
    getpass = LazyModule("getpass")
    hashlib = LazyModule("hashlib")
    Bytes = LazyProperty(".bytes", "Bytes")

newline = "\n"
newline2 = "\r\n"


class Str:
    """Class with functions for managing strings."""

    value: str

    def __getattribute__(self, name: str) -> Any:
        """Proxy selected methods to classmethod helpers."""
        instance_forward = {"to_quotes", "to_quotes_2", "split_every", "leftpad", "rightpad"}
        if name in instance_forward:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                result = getattr(self.__class__, name)(self.value, *args, **kwargs)
                if name in {"to_quotes", "to_quotes_2", "leftpad", "rightpad"}:
                    self.value = result
                return result
            return _wrapper
        return object.__getattribute__(self, name)

    def __init__(self, value: Any = "") -> None:
        self.value = str(value)

    @classmethod
    def to_quotes(cls, some_string: Any) -> str:
        """Wrap a value in double quotes.

        <br>`param some_string` string
        <br>`return` string, inside "" quotes
        """
        return '"' + str(some_string) + '"'

    @classmethod
    def to_quotes_2(cls, some_string: Any) -> str:
        """Wrap a value in single quotes.

        <br>`param some_string` string
        <br>`return` string, inside '' quotes
        """
        return "'" + str(some_string) + "'"

    @classmethod
    def get_integers(
        cls,
        string: Any,
        float_support: bool = True,
        debug: bool = False
    ) -> List[Union[int, float]]:
        """Extract integers (and floats optionally) from a string.

        <br>`param string` string, with some integers or floats inside
        <br>`param float_support` boolean, enable float support
        <br>`param debug` boolean, debug print enable
        <br>`return` list of integers or floats
        """
        string = cls.remove_spaces(string)
        integer_found = False
        integers: List[Union[int, float]] = []
        current_integer: float = 0.0
        negative = False
        float_numbers: Optional[int] = None
        for symbol in str(string) + " ":  # in exception some processing, meh :(
            try:
                if symbol in ['-', '—'] and not integer_found:
                    negative = True
                    continue
                if float_support:
                    if symbol in [".", ","]:
                        if isinstance(float_numbers, int):
                            float_numbers = None
                            raise ValueError  # goto to except block code
                        float_numbers = 0
                        continue
                int(symbol)
                if isinstance(float_numbers, int):
                    float_numbers += 1
                    value_before = current_integer
                    added_value = int(symbol)*pow(10, -float_numbers)
                    current_integer = current_integer + added_value
                    if debug:
                        print("value_before", value_before, "float_numbers", float_numbers, "added_value", added_value,
                              "current_integer", current_integer)
                    current_integer = round(current_integer, float_numbers)  # to reduce problems with floating numbers
                else:
                    current_integer = current_integer*10 + int(symbol)
                integer_found = True
            except ValueError:
                if integer_found:
                    if negative:
                        current_integer = -current_integer
                    integers = integers + [current_integer]
                    current_integer = 0.0
                    integer_found = False
                negative = False
                float_numbers = None
        return integers

    @classmethod
    def newlines_to_strings(cls, string: str) -> List[str]:
        """Split a string by newlines.

        <br>`param string` string, with some newlines
        <br>`param verbose` boolean suppress print to console
        <br>`return` list of strings
        """
        if isinstance(string, str):  # if input is string
            string = string.replace(newline2, newline)
            strings = string.split(newline)
            return strings
        else:
            raise TypeError(str(type(string)) + " can't be split")

    @classmethod
    def nl(cls, string: str) -> List[str]:  # pylint: disable=invalid-name
        """Split a string by newlines.

        <br>`param string` string, with some newlines
        <br>`param verbose` boolean suppress print to console
        <br>`return` list of strings
        """
        return cls.newlines_to_strings(string=string)

    @classmethod
    def split_every(cls, string: Union[int, str], chars: int, reverse: bool = False) -> List[str]:
        """Split a string every N chars.

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
        char_exists = "."
        char_can_be_exists = ".?"
        regexp = char_exists + char_can_be_exists*(chars-1)
        if reverse:
            string = string[::-1]
        output = re.findall(regexp, string, re.DOTALL)
        if reverse:
            output = list(reversed(output))
            output = [s[::-1] for s in output]
        return output

    @classmethod
    def leftpad(cls, string: Any, length: int, char: Any = "0", rightpad: bool = False) -> str:
        """Add padding characters to the left of a string.

        <br>`param string` string, input
        <br>`param length` int, len of output string
        <br>`param char` string, characters, added to left side of input string
        <br>`param rightpad` boolean, if True, adds symbols to right side
        <br>`return` string, with added characters to side of input string
        """
        char_value = str(char)
        string_value = str(string)
        if len(string_value) >= length:
            return string_value
        str_of_chars = char_value * int((length/len(char_value))+1)
        string_output = str_of_chars[len(string_value):length] + string_value
        if rightpad:
            string_output = string_value + str_of_chars[len(string_value):length]
        return string_output

    @classmethod
    def rightpad(cls, string: Any, length: int, char: Any = "0") -> str:
        """Add padding characters to the right of a string.

        <br>`param string` string, input
        <br>`param length` int, len of output string
        <br>`param char` string, characters, added to right side of input string
        <br>`return` string, with added characters to side of input string
        """
        return cls.leftpad(string, length, char=char, rightpad=True)

    @classmethod
    def substring(
        cls,
        string: Union[str, bytes, Any],
        before: Union[str, bytes, Any],
        after: Optional[Union[str, bytes, Any]] = None,
        return_after_substring: bool = False,
        safe: bool = False,
        exception_message: Optional[str] = None
    ) -> Union[str, Tuple[str, str]]:
        """Get substring between "before" and "after" markers.

        <br>`param string` string
        <br>`param before` string, that before output string
        <br>`param after` string, that after output string
        <br>`param return_after_substring` boolean, if True, return list of substring and part after substring
        <br>`param safe` boolean, suppress exceptions if something not found
        <br>`param exception_message` string, will be in exception that raised
        <br>`return` string, from string that between "before", and "after" arguments
        """
        if isinstance(string, bytes):
            string = Bytes.to_string(string)
        if isinstance(before, bytes):
            before = Bytes.to_string(before)
        if isinstance(after, bytes):
            after = Bytes.to_string(after)
        if not isinstance(string, str):
            string = str(string)
        if not isinstance(before, str):
            before = str(before)
        if after is not None and not isinstance(after, str):
            after = str(after)
        start_from = string.find(before)
        after_substring = ""
        if start_from != -1:
            start_from = string.find(before) + len(before)
        else:
            start_from = 0
            if not safe:
                if isinstance(exception_message, str):
                    exception_message += '. '
                elif exception_message is None:
                    exception_message = ""
                raise KeyError(f'{exception_message}The line preceding "{before}" the search string was not found')
        if after:
            end_at = string[start_from:].find(after)
            if end_at != -1:
                end_at += start_from
                substring = string[start_from:end_at]
                if return_after_substring:
                    after_substring = string[end_at:]
            else:
                substring = string[start_from:]
                if return_after_substring:
                    after_substring = ""
                if not safe:
                    if isinstance(exception_message, str):
                        exception_message += '. '
                    elif exception_message is None:
                        exception_message = ""
                    raise KeyError(f'{exception_message}The string '
                                   f'"{after}" that followed the search string was not found')
        else:
            substring = string[start_from:]
        if return_after_substring:
            return substring, after_substring
        return substring

    @classmethod
    def diff_simple(cls, string_a: str, string_b: str) -> None:
        """Print different symbols between two strings.

        <br>`param string_a` string
        <br>`param string_b` string
        <br>`return` None
        """
        strings = [(string_a, string_b)]  # for further support for unlimited strings
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

    @classmethod
    def input_pass(cls, string: str = "Password:") -> str:
        """Read a password securely from input.

        <br>`param string` string, with message to user, that asks password
        <br>`return` string, that returned from getpass lib
        """
        return getpass.getpass(str(string))

    @classmethod
    def input_int(
        cls,
        message: str = "Input integer: ",
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        default: Optional[int] = None,
        debug: bool = True
    ) -> int:
        """Ask the user to input an integer.

        <br>`param message` string, message to user
        <br>`param minimum` minimum value of returned integer
        <br>`param maximum` maximum value of returned integer
        <br>`param default` default value if user just press Enter
        <br>`param debug` boolean, debug purposes
        <br>`return` int, input from user
        """
        output_int: Optional[int] = None
        if default:
            message += "(Enter = " + str(default) + ") "
        while output_int is None:  # cycle while integer is not provided
            raw = input(message)
            if raw != "":
                try:
                    parsed = int(cls.get_integers(raw)[0])
                except IndexError:
                    print("It's not an integer")
                    continue
            elif default is not None and raw == "":
                output_int = default
                break
            else:
                print("It's not an integer")
                raise ValueError
            if minimum is not None:
                if parsed < minimum:
                    print("Value must be greater than", minimum)
                    raise ValueError
            if maximum is not None:
                if parsed > maximum:
                    print("Value must be less than", maximum)
                    raise ValueError
            output_int = parsed
            break
        if debug:
            print("Output integer:", output_int)
        assert output_int is not None
        return output_int

    @classmethod
    def remove_spaces(cls, string_: Any) -> str:
        """Remove duplicate spaces in a string.

        <br>`param string_` string, input
        <br>`return` string, without duplicated spaces
        """
        string_value = str(string_)
        while '  ' in string_value:
            string_value = string_value.replace('  ', ' ')
        return string_value

    @classmethod
    def get_words(cls, string_: str) -> List[str]:
        """Split a string into words by spaces.

        <br>`param string_` string, with spaces to split it
        <br>`return` list of substrings, split by space|multiple space
        """
        removed_spaces = ' '.join(string_.split())  # at least, it's fast https://stackoverflow.com/questions/2077897/
        # substitute-multiple-whitespace-with-single-whitespace-in-python
        words = removed_spaces.split(" ")
        if words == [""]:
            words = []
        return words

    @classmethod
    def guid_from_seed(cls, seed: str) -> str:
        """Generate a GUID-like string from a seed.

        <br>`param seed` string, seed to generate guid
        <br>`return` string, guid-like
        """
        bytes_seed = bytes(seed, "utf-8")
        hash_sha256 = hashlib.sha256(bytes_seed)
        hash_hex_digest = hash_sha256.hexdigest()
        str_hash_hex = str(hash_hex_digest)
        symbols = str_hash_hex.zfill(32)[-32:]  # adds zeros if needed and cut unneeded symbols
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string

    @classmethod
    def encrypt(cls, string: str, password: str) -> List[int]:
        """Encrypt a string with a password into an int list."""
        int_list: List[int] = []
        password_len = len(password)
        for cnt, sym in enumerate(string):
            password_sym = password[cnt % password_len]
            int_list.append(ord(sym) - ord(password_sym))
        return int_list

    @classmethod
    def decrypt(cls, int_list: List[int], password: str) -> str:
        """Decrypt an int list into a string using a password."""
        output_string = ""
        password_len = len(password)
        for cnt, numb in enumerate(int_list):
            password_sym = password[cnt % password_len]
            chr_number = numb + ord(password_sym)

            try:
                char = chr(chr_number)
            except ValueError:
                if chr_number > 0x10FFFF:
                    char = chr(0x10FFFF)
                else:
                    char = chr(0)
            output_string += char

        return output_string

    seeds: List[str] = []

    @classmethod
    def guid_by_seed(cls, seed: str, uniq_in_process: bool = True) -> str:
        """Generate a GUID-like string and optionally enforce uniqueness."""
        if seed in cls.seeds:
            if uniq_in_process:
                raise KeyError(fr"seed '{seed}' already used by guid_by_seed")
        else:
            cls.seeds.append(seed)
        bytes_seed = bytes(seed, "utf-8")
        hash_sha256 = hashlib.sha256(bytes_seed)
        hash_hex_digest = hash_sha256.hexdigest()
        str_hash_hex = str(hash_hex_digest)
        symbols = str_hash_hex.zfill(32)[-32:]  # adds zeros if needed and cut unneeded symbols
        string = symbols[:8] + "-" + symbols[8:12] + "-" + symbols[12:16] + "-" + symbols[16:20] + "-" + symbols[20:]
        return string


    @classmethod
    def rreplace(cls, string: str, old: str, new: str, occurrence: int) -> str:
        """Replace occurrences from the right.

        :param string: str, string, where to replace
        :param old: str, substring to replace
        :param new: str, substring to insert
        :param occurrence: int, count of replacement from right
        :return: str, string with replaced substrings
        """
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

    @classmethod
    def is_ascii(cls, string: str) -> bool:
        """Return True if a string is ASCII-only."""
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    python_encodings: List[str] = [
        'ascii', 'big5', 'big5hkscs', 'cp037', 'cp424', 'cp437', 'cp500', 'cp737', 'cp775', 'cp850',
        'cp852', 'cp855', 'cp856', 'cp857', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865',
        'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1140',
        'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258',
        'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz',
        'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3',
        'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
        'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14',
        'iso8859_15', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic', 'mac_greek', 'mac_iceland',
        'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004',
        'shift_jisx0213', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8'
    ]
