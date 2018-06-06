#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with mouse
"""
__version__ = "1.2.8"

try:
    import pyautogui
except ImportError:
    from .installreq8 import pyautogui


class SettingsMouse:  # pylint: disable=too-few-public-methods
    """Some settings
    """
    mouse_move_duration = 0.5
    sleep_before_click = 0.1

    @classmethod
    def set_mouse_move_duration(cls, seconds):
        """
        :param seconds: int|float, seconds to move mouse
        :return: None
        """
        cls.mouse_move_duration = seconds


class Mouse:  # pylint: disable=too-few-public-methods
    """Class with functions to work with mouse
    """
    class Scroll:  # doesnt work good at new Windows >= 8
        """Class with functions to scroll
        """
        @staticmethod
        def scroll(value, up):  # pylint: disable=invalid-name
            """
            :param value: int, how much to scroll, idk, how it work
            :param up: boolean, scroll up or down
            :return:
            """
            value = int(value)
            if not up:
                value = 0-value
            pyautogui.vscroll(clicks=value)
            print("scrolled", value)

        @classmethod
        def up(cls, value=100):  # pylint: disable=invalid-name
            """
            :param value: int, how much to scroll, idk, how it work
            :return:
            """
            cls.scroll(value, up=True)

        @classmethod
        def down(cls, value=100):
            """
            :param value: int, how much to scroll, idk, how it work
            :return:
            """
            cls.scroll(value, up=False)

    class Click:
        """Class with click mouse functions
        """
        @staticmethod
        def click(button, position, quiet=False):
            """
            :param button: string with button name
            :param position: list with two values x and y (pixels from up and left)
            :param quiet: boolean, suppress print to console
            :return: None
            """
            from .time8 import Time
            Time.sleep(SettingsMouse.sleep_before_click, quiet_small=quiet)
            if position:
                pyautogui.click(x=position[0], y=position[1], button=button)
            else:
                pyautogui.click(button=button)
            if not quiet:
                print("click mouse " + button)

        @classmethod
        def right(cls, position=None, quiet=False):
            """
            :param position: list with two values x and y (pixels from up and left)
            :param quiet: boolean, suppress print to console
            :return: None
            """
            cls.click(button='right', position=position, quiet=quiet)

        @classmethod
        def left(cls, position=None, quiet=False):
            """
            :param position: list with two values x and y (pixels from up and left)
            :param quiet: boolean, suppress print to console
            :return: None
            """
            cls.click(button='left', position=position, quiet=quiet)

    @staticmethod
    def move(x, y, x2=None, y2=None,  # pylint: disable=too-many-arguments, invalid-name
             duration=SettingsMouse.mouse_move_duration, tween=pyautogui.easeInOutQuad, rel=False, quiet=False):
        """
        :param x: int, position in pixels
        :param y: int, position in pixels
        :param x2: int, used if position is rectangle, so center will be found
        :param y2: int, used if position is rectangle, so center will be found
        :param duration: float|int, time to move mouse
        :param tween: tween from pyautogui
        :param rel: boolean, move relatively
        :param quiet: boolean, suppress print to console
        :return: None
        """
        if isinstance(x, tuple):
            if len(x) == 2:
                y = x[1]
                x = x[0]
            elif len(x) == 4:
                y = x[1]
                x2 = x[2]
                y2 = x[3]
                x = x[0]
        if x2 and y2:
            x, y = pyautogui.center((x, y, x2, y2))
        if not quiet:
            if rel:
                how = "relative"
            else:
                how = "to"
            print("moved mouse", how, x, y)

        if rel:
            pyautogui.moveRel(x, y, duration=duration, tween=tween)
        else:
            pyautogui.moveTo(x, y, duration=duration, tween=tween)
