#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with commandline interfaces
"""
__version__ = "0.2.2"


class CLI:
    """Class to work with commandline interfaces
    """
    @staticmethod
    def get_y_n(question, default=None):
        """Obtain answer yes or no from user in commandline.
        <br>`param question` string with question to user
        <br>`param answer` predefined string with answer, must be "y" or "n"
        <br>`return` boolean
        """
        def check_answer(string):  #pylint: disable=inconsistent-return-statements
            """Check input from user or argument "answer"
            <br>`param string` input string, check answer for "y" or "n", for other values return None
            <br>`return` True|False|None
            """
            if string is None:
                return
            if string.lower() == "y":
                return True
            if string.lower() == "n":
                return False
            return

        while True:
            print_str = f"{question} (y/n)?"
            if default:
                print_str += " default '{default}'"
            input_str = input(print_str)
            input_str = input_str.strip()
            output = check_answer(input_str)
            if output is not None:
                return output
            elif check_answer(default) is not None:
                return check_answer(default)

    @staticmethod
    def get_ints(question, count_of_ints, answer=None):
        """Obtain answer with integers from user in commandline.
        <br>`param question` string with question to user
        <br>`param count_of_ints` int of ints must be in answer
        <br>`param answer` predefined string with answer
        <br>`return` integer or list of integers
        """

        def check_answer(input, count_of_ints):  # pylint: disable=inconsistent-return-statements
            """Check input from user or argument "answer"
            <br>`param input` input string
            <br>`param count_of_ints` int of ints must be in answer
            <br>`return` True|False|None
            """
            from .str9 import Str
            ints = Str.get_integers(input, float_support=False)
            if len(ints) == count_of_ints:
                if count_of_ints == 1:
                    return ints[0]
                return ints
            return

        if answer:
            output = check_answer(answer, count_of_ints)
            if output is not None:
                return output
        while True:
            input_str = input(f"{question} (answer {count_of_ints} integer_s)?")
            input_str = input_str.strip(" ")
            output = check_answer(input_str, count_of_ints)
            if output is not None:
                return output

    @classmethod
    def get_int(cls, question, answer=None):
        return cls.get_ints(question=question, count_of_ints=1, answer=answer)

    wait_update_pos = 0

    @classmethod
    def wait_update(cls, quiet=False):
        """Print 'spinning' (if function called multiple times) stick, used for long processes to show user that some
        progress are going.
        <br>`param quiet` boolean, suppress print to console
        <br>`return` string with 'stick' in new position
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
        <br>`param count` int|float current progress status value
        <br>`param finish` int|float finish progress value
        <br>`param width_of_output` int width of progressbar, by default it's width of console
        <br>`return`
        """
        raise NotImplementedError
        from .console9 import Console  # pylint: disable=unreachable
        Console.width()
