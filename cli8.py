#! python3
# -*- coding: utf-8 -*-
__version__ = "0.0.3"


class CLI:
    @staticmethod
    def get_y_n(question="", answer=None):
        def check_answer(string):
            if inputtt == "y":
                return True
            if inputtt == "n":
                return False

        if answer:
            check_answer(answer)
        while True:
            inputtt = input(str(question) + " (y/n)?")
            inputtt = inputtt.strip(" ")
            check_answer(inputtt)

    wait_update_pos = 0

    @classmethod
    def wait_update(CLI, quiet=False):
        if CLI.wait_update_pos == 0:
            stick = "|"
        elif CLI.wait_update_pos == 1:
            stick = "/"
        elif CLI.wait_update_pos == 2:
            stick = "-"
        elif CLI.wait_update_pos == 3:
            stick = "\ "[:1]
        elif CLI.wait_update_pos == 4:
            stick = "|"
        elif CLI.wait_update_pos == 5:
            stick = "/"
        elif CLI.wait_update_pos == 6:
            stick = "-"
        elif CLI.wait_update_pos == 7:
            stick = "\ "[:1]
            CLI.wait_update_pos = -1
        CLI.wait_update_pos += 1
        if not quiet:
            from .print8 import Print
            Print.rewrite(stick)
            return stick
        else:
            return stick

    @staticmethod
    def progressbar(count, of):
        raise NotImplementedError
        Console.width()
