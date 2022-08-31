#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with commandline interfaces
"""
__version__ = "0.4.10"


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

        def check_answer(string):  # pylint: disable=inconsistent-return-statements
            """Check input from user or argument "answer"
            <br>`param string` input string, check answer for "y" or "n", for other values return None
            <br>`return` True|False|None
            """
            from .keyboard9 import Keyboard
            import thefuck.const

            if string is None:
                return

            if isinstance(string, thefuck.const._GenConst):
                string_t = string._name
                if string == thefuck.const.KEY_CTRL_C:
                    raise KeyboardInterrupt
            else:
                string = string.lower()
                string_t = Keyboard.translate_string(string)

            if string != string_t:
                print(" > " + string_t, end="")
                string = string_t

            if string == "y":
                return True
            if string == "n":
                return False
            return

        while True:
            print_str = f"{question} (y/n)? "
            if default:
                print_str += f" default '{default}'"
            try:
                import thefuck.system
                print(print_str, end="", flush=True)
                input_str = thefuck.system.get_key()
                print(input_str, end="")
            except Exception:
                input_str = input(print_str)
                input_str = input_str.strip()
            output = check_answer(input_str)
            print()
            if output is not None:
                return output
            elif check_answer(default) is not None:
                return check_answer(default)

    @staticmethod
    def get_ints(question, count_of_ints):
        """Obtain answer with integers from user in commandline.
        <br>`param question` string with question to user
        <br>`param count_of_ints` int of ints must be in answer
        <br>`param answer` predefined string with answer
        <br>`return` integer or list of integers
        """
        from .str9 import Str

        while True:
            input_str = input(f"{question} (answer {count_of_ints} integer_s): ")
            ints = Str.get_integers(input_str, float_support=False)
            output = None
            if len(ints) == count_of_ints:
                if count_of_ints == 1:
                    output = ints[0]
                else:
                    output = ints
            if output is not None:
                return output

    @classmethod
    def get_int(cls, question):
        return cls.get_ints(question=question, count_of_ints=1)

    wait_update_pos = 0

    @classmethod
    def wait_update(cls, quiet=False):
        """Print 'spinning' (if function called multiple times) stick, used for long processes to show user that some
        progress are going.
        <br>`param quiet` boolean, suppress print to console
        <br>`return` string with 'stick' in new position
        """
        from .const9 import backslash
        stick = None
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
        <br>`param width_of_output` int width of progressbar, by default its width of console
        <br>`return`
        """
        raise NotImplementedError
        from .console9 import Console  # pylint: disable=unreachable
        Console.width()

    @staticmethod
    def multiline_input(question: str) -> str:
        print("\nEnter|paste your content. Ctrl-D or Ctrl-Z (Windows) to save it.")
        print(question)
        lines = []
        while True:
            try:
                lines.append(input())
            except EOFError:
                print()
                break
        return "\n".join(lines)

    @staticmethod
    def get_date(date_name: str, always_return_date: bool = False):
        """Gets date from user input.

        :param date_name: string, name of date for user
        :param always_return_date: bool, ask user a date until valid is entered
        :return None if date is not entered and always_return_date is False
        :return datetime.datetime if correct data is entered (time is 00:00:00)"""
        from .time9 import Time
        date = None
        while date is None:
            date_str = input(f"Enter date of {date_name} like \"{str(Time.datetime().day).zfill(2)}\" "
                             f"or with month \"{str(Time.datetime().day).zfill(2)}"
                             f"{str(Time.datetime().month).zfill(2)}\" "
                             f"or with year \"{str(Time.datetime().day).zfill(2)}"
                             f"{str(Time.datetime().month).zfill(2)}"
                             f"{str(Time.datetime().year).zfill(4)}\": ").strip()
            if date_str:
                date = Time.datetime()
                try:
                    day = int(date_str[:2])
                except ValueError:
                    day = date.day
                try:
                    month = int(date_str[2:4])
                except ValueError:
                    month = date.month
                try:
                    year = int(date_str[4:])
                    if len(str(year)) == 2:
                        year += 2000
                except ValueError:
                    year = date.year

                try:
                    date = date.replace(day=day, month=month, year=year, hour=0, minute=0, second=0, microsecond=0)
                    break
                except ValueError:
                    print("Wrong date.")
                    date = None
            else:
                if always_return_date:
                    print("Please, enter date.")
                    continue
                else:
                    break

        return date
