#! python3
# -*- coding: utf-8 -*-
"""Internal module with functions to work with mouse
"""
__version__ = "1.6.0"


class SettingsMouse:  # pylint: disable=too-few-public-methods
    """Some settings
    """
    mouse_move_duration = 0.5
    sleep_before_click = 0.1

    @classmethod
    def set_mouse_move_duration(cls, seconds):
        """
        <br>`param seconds` int|float, seconds to move mouse
        <br>`return` None
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
            <br>`param value` int, how much to scroll, idk, how it work
            <br>`param up` boolean, scroll up or down
            <br>`return`
            """
            import pyautogui

            value = int(value)
            if not up:
                value = 0-value
            pyautogui.vscroll(clicks=value)
            print("scrolled", value)

        @classmethod
        def up(cls, value=100):  # pylint: disable=invalid-name
            """
            <br>`param value` int, how much to scroll, idk, how it work
            <br>`return`
            """
            cls.scroll(value, up=True)

        @classmethod
        def down(cls, value=100):
            """
            <br>`param value` int, how much to scroll, idk, how it work
            <br>`return`
            """
            cls.scroll(value, up=False)

    class Click:
        """Class with click mouse functions
        """
        @staticmethod
        def click(button, position, quiet=False, sleep_before_click=SettingsMouse.sleep_before_click):
            """
            <br>`param button` string with button name
            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param quiet` boolean, suppress print to console
            <br>`return` None
            """
            import pyautogui

            from .time9 import Time
            Time.sleep(sleep_before_click, verbose=not quiet)
            if position:
                pyautogui.click(x=position[0], y=position[1], button=button)
            else:
                pyautogui.click(button=button)
            if not quiet:
                print("click mouse " + button)

        @classmethod
        def right(cls, position=None, quiet=False, sleep_before_click=SettingsMouse.sleep_before_click):
            """
            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param quiet` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='right', position=position, quiet=quiet, sleep_before_click=sleep_before_click)

        @classmethod
        def left(cls, position=None, quiet=False, sleep_before_click=SettingsMouse.sleep_before_click):
            """
            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param quiet` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='left', position=position, quiet=quiet, sleep_before_click=sleep_before_click)

        @classmethod
        def middle(cls, position=None, quiet=False, sleep_before_click=SettingsMouse.sleep_before_click):
            """
            <br>`param position` list with two values x and y (pixels from up and left)
            <br>`param quiet` boolean, suppress print to console
            <br>`return` None
            """
            cls.click(button='middle', position=position, quiet=quiet, sleep_before_click=sleep_before_click)

    @staticmethod
    def move(x, y=None, x2=None, y2=None,  # pylint: disable=too-many-arguments, invalid-name
             duration=SettingsMouse.mouse_move_duration, tween=None, rel=False, quiet=False):
        """
        <br>`param x` int, position in pixels
        <br>`param y` int, position in pixels
        <br>`param x2` int, used if position is rectangle, so center will be found
        <br>`param y2` int, used if position is rectangle, so center will be found
        <br>`param duration` float|int, time to move mouse
        <br>`param tween` tween from pyautogui
        <br>`param rel` boolean, move relatively
        <br>`param quiet` boolean, suppress print to console
        <br>`return` None
        """
        import pyautogui

        if tween is None:
            tween = pyautogui.easeInOutQuad
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

    @staticmethod
    def get_position():
        """
        <br>`return` typle, x and y position of mouse
        """
        import pyautogui

        return pyautogui.position()