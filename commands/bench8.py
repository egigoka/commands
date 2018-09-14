#! python3
# -*- coding: utf-8 -*-
"""Internal module with Bench factory function
"""
__version__ = "0.5.1"


class Bench:
    """Benchmarking class (not so good, but enough for some purposes)
    """

    def __init__(self, prefix="Bench passed in", quiet=False, fraction_digits=3, time_start=None):
        """
        :param prefix: string, prints when ending of benchmark
        :param quiet: boolean, suppress output to console
        :param fraction_digits: integer, define how much digits after dot print
        :param time_start: datetime.datetime, set custom start time
        """
        import datetime
        if time_start:
            self.time_start = time_start
        else:
            self.time_start = datetime.datetime.now()
        self.time_end = None
        self.quiet = quiet
        self.prefix = prefix
        self.fraction_digits = fraction_digits

    def start(self):  # set time of begin to now
        """Set time of start benchmarking to current
        :return: None
        """
        import datetime
        self.time_start = datetime.datetime.now()

    def get(self):
        """
        :return: float, time difference between start and this function call time
        """
        import datetime
        from .time8 import Time
        self.time_end = datetime.datetime.now()
        return Time.delta(self.time_start, self.time_end)

    def end(self, prefix_string=None, quiet_if_zero=False, start_immediately=False):
        """End benchmarking:
        return time difference between start and end of bencmarking, print string with prefix
        and time difference.
        :param prefix_string: string, used in print output
        :param quiet_if_zero: suppress print if time interval between start and stop = 0.0 in accuracy, defined in
        cls.fraction_digits
        :param start_immediately: change start time of current Bench class to current time
        :return: float, delta between start and end
        """
        delta = self.get()
        self.start()
        if prefix_string:
            self.prefix = prefix_string
        if not self.quiet:
            # print(not quiet_if_zero, str(round(delta, cls.fraction_digits)),
            # (str(round(delta, cls.fraction_digits)) != "0.0"),
            # (not quiet_if_zero) and (str(round(delta, cls.fraction_digits)) != "0.0"))
            if (not quiet_if_zero) or (str(round(delta, self.fraction_digits)) != "0.0"):
                try:
                    from .print8 import Print
                    Print.colored(self.prefix, str(round(delta, self.fraction_digits)), "seconds", "grey", "on_white")
                except TypeError:
                    print(self.prefix, str(round(delta, self.fraction_digits)), "seconds")
                except AttributeError:
                    print(self.prefix, str(round(delta, self.fraction_digits)), "seconds")
        if start_immediately:
            self.start()
        return delta
