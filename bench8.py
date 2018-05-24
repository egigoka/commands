#! python3
# -*- coding: utf-8 -*-
"""Internal module with Bench factory function
"""
__version__ = "0.4.2"


def get_Bench():  # pylint: disable=invalid-name
    """
    :return: class Bench
    """
    class Bench(object):
        """Benchmarking class (not so good, but enough for some purposes)
        """
        import datetime
        time_start = datetime.datetime.now()
        time_end = None
        quiet = False  # d argument for disable print to terminal
        prefix = "Bench passed in"  # d what have been done, will print if
        fraction_digits = 3  # how much digits after dot print

        @classmethod
        def start(cls):  # set time of begin to now
            """Set time of start benchmarking to current
            :return: None
            """
            import datetime
            cls.time_start = datetime.datetime.now()

        @classmethod
        def get(cls):
            """
            :return: float, time difference between start and this function call time
            """
            import datetime
            from .time8 import Time
            cls.time_end = datetime.datetime.now()
            return Time.delta(cls.time_start, cls.time_end)

        @classmethod
        def end(cls, prefix_string=None, quiet_if_zero=False, start_immediately=False):
            """End benchmarking:
            return time difference between start and end of bencmarking, print string with prefix
            and time difference.
            :param prefix_string: string, used in print output
            :param quiet_if_zero: suppress print if time interval between start and stop = 0.0 in accuracy, defined in
            cls.fraction_digits
            :param start_immediately: change start time of current Bench class to current time
            :return: float, delta between start and end
            """
            delta = cls.get()
            cls.start()
            if prefix_string:
                cls.prefix = prefix_string
            if not cls.quiet:
                # print(not quiet_if_zero, str(round(delta, cls.fraction_digits)),
                # (str(round(delta, cls.fraction_digits)) != "0.0"),
                # (not quiet_if_zero) and (str(round(delta, cls.fraction_digits)) != "0.0"))
                if (not quiet_if_zero) or (str(round(delta, cls.fraction_digits)) != "0.0"):
                    try:
                        from .print8 import Print
                        Print.colored(cls.prefix, str(round(delta, cls.fraction_digits)), "seconds", "grey", "on_white")
                    except TypeError:
                        print(cls.prefix, str(round(delta, cls.fraction_digits)), "seconds")
                    except AttributeError:
                        print(cls.prefix, str(round(delta, cls.fraction_digits)), "seconds")
            if start_immediately:
                cls.start()
            return delta
    return Bench
