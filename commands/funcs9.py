#! python3
# -*- coding: utf-8 -*-
"""Internal module with shit functions
"""
__version__ = "3.4.3"


class Q:
    def __repr__(self):
        raise SystemExit

    def __call__(self, code=None):
        import _sitebuiltins
        quitter = _sitebuiltins.Quitter("q", "end of file? wtf? why it's string?")
        quitter.__call__(code)


def dirify(_object, wildcard="*"):
    """Print and return list of object public attributes
    <br>`param object_` object to input
    <br>`param regexp` string with shell-like wildcards for filtering
    <br>`param quiet` suppress output to console
    <br>`return` None
    """
    from .list9 import List
    from .str9 import Str
    longest_name = 0
    attrs = List.wildcard_search(dir(_object), wildcard)
    for attr_str in attrs:
        if len(attr_str) > longest_name:
            longest_name = len(attr_str)
    for attr_str in attrs:
        try:
            _type = type(_object.__getattribute__(attr_str))
        except TypeError:
            _type = type(_object.__getattribute__(_object, attr_str))
        except AttributeError:
            _type = "AttributeError happened"
        except OSError:
            _type = "OSError happened"
        _type = Str.substring(str(_type), "<class ", ">", safe=True)
        print(f"{Str.rightpad(attr_str, longest_name, '—')}>{_type}")


def multiple(*types):
    from typing import Union
    return Union[types]

def copy(string: str):
    import pyperclip
    pyperclip.copy(string)

def paste():
    import pyperclip
    return pyperclip.paste()

q = Q()
exit = Q()
