#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with commandline interfaces
"""
__version__ = "0.0.9"


class CLI:
    """Class to work with commandline interfaces
    """
    @staticmethod
    def get_y_n(question, answer=None):
        """Obtain answer yes or no from user in commandline.
        :param question: string with question to user
        :param answer: predefined string with answer, must be "y" or "n"
        :return: boolean
        """
        def check_answer(string):  #pylint: disable=inconsistent-return-statements
            """Check input from user or argument "answer"
            :param string: input string, check answer for "y" or "n", for other values return None
            :return: True|False|None
            """
            if string.lower() == "y":
                return True
            if string.lower() == "n":
                return False

        if answer:
            output = check_answer(answer)
            if output is not None:
                return output
        while True:
            inputtt = input(str(question) + " (y/n)?")
            inputtt = inputtt.strip(" ")
            output = check_answer(inputtt)
            if output is not None:
                return output

    wait_update_pos = 0

    @classmethod
    def wait_update(cls, quiet=False):
        """Print 'spinning' (if function called multiple times) stick, used for long processes to show user that some
        progress are going.
        :param quiet: boolean, suppress print to console
        :return: string with 'stick' in new position
        """
        from .const9 import backslash
        if cls.wait_update_pos == 0:
            stick = "|"
        elif cls.wait_update_pos == 1:
            stick = "/"
        elif cls.wait_update_pos == 2:
            stick = "-"
        elif cls.wait_update_pos == 3:
            stick = backslash
            cls.wait_update_pos = -1
        cls.wait_update_pos += 1
        if not quiet:
            from .print9 import Print
            Print.rewrite(stick)
        return stick

    @staticmethod
    def progressbar(count, finish, width_of_output=None):
        """Here must be realisation of progressbar
        :param count: int|float current progress status value
        :param finish: int|float finish progress value
        :param width_of_output: int width of progressbar, by default it's width of console
        :return:
        """
        raise NotImplementedError
        from .console9 import Console  # pylint: disable=unreachable
        Console.width()
