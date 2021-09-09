#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with time
"""
__version__ = "1.1.0"


class Time:
    """Class to work with time
    """
    @staticmethod
    def __lp2(string, length=2):
        """Internal alias to Str.leftpad
        """
        from .str9 import Str
        return Str.leftpad(string, length, 0)

    @staticmethod
    def stamp():
        """
        <br>`return` float, timestamp
        """
        import time
        return time.time()
    
    @staticmethod
    def datetime(year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, tzinfo=None, fold=None):
        import datetime
        now = datetime.datetime.now()
        args = {}
        if year is not None:
            args["year"] = year
        if month is not None:
            args["month"] = month
        if day is not None:
            args["day"] = day
        if hour is not None:
            args["hour"] = hour
        if minute is not None:
            args["minute"] = minute
        if second is not None:
            args["second"] = second
        if microsecond is not None:
            args["microsecond"] = microsecond
        if tzinfo is not None:
            args["tzinfo"] = tzinfo
        if fold is not None:
            args["fold"] = fold
        datetime_datetime = now.replace(**args)
        return datetime_datetime

    @staticmethod
    def timestamp_to_datetime(timestamp):
        """
        <br>`param timestamp` float, timestamp
        <br>`return` datetime.datetime time object
        """
        import datetime
        if isinstance(timestamp, (str, int)):
            timestamp = float(timestamp)
        elif isinstance(timestamp, float):
            pass
        elif isinstance(timestamp, datetime.datetime):
            return timestamp
        else:
            raise TypeError(f"timestamp must be float, int or str, not {type(timestamp)}")
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def datetime_to_timestamp(datetime_object):
        """
        <br>`param datetime_object` datetime.datetime time object
        <br>`return` float, timestamp
        """
        import time
        if isinstance(datetime_object, float):
            return datetime_object
        return time.mktime(datetime_object.timetuple())

    @classmethod
    def dotted(cls, custom_time=None):
        """
        <br>`param custom_time` datetime.datetime time object|float of timestamp
        <br>`return` string with time in format "1999.12.31_at_12.59.59.999999"
        """
        import datetime
        if custom_time:
            time = cls.timestamp_to_datetime(custom_time)
        else:
            time = datetime.datetime.now()
        time = cls.__lp2(time.year) + "." + cls.__lp2(time.month) + "." + cls.__lp2(time.day) + "_at_" + \
            cls.__lp2(time.hour) + "." + cls.__lp2(time.minute) + "." + cls.__lp2(time.second) + "." + \
            cls.__lp2(time.microsecond, 6)
        return time

    @staticmethod
    def _timer(seconds, check_per_sec=10):
        """Internal function to idle (used in Time.sleep). Print how much time left.
        <br>`param seconds` int|float, how long sleep
        <br>`param check_per_sec` int|float, how often check time
        <br>`return` None
        """
        from .print9 import Print
        from .bench9 import Bench
        benchmark = Bench()
        secs_second_var = int(seconds)
        while benchmark.get() < seconds:
            import time
            time.sleep(1/check_per_sec)

            secs_left_int = int(seconds - benchmark.get())

            if secs_left_int != secs_second_var:
                secs_second_var = secs_left_int
                string = "Timer for " + str(seconds) + " seconds."
                if seconds > 1:
                    string += " " + str(secs_left_int) + " left"
                Print.rewrite(string)

        Print.rewrite("")

    @classmethod
    def sleep(cls, seconds, verbose=False, check_per_sec=10):
        """Function to idle. If 'seconds more, than 1, running Time._timer. Otherwise run time.sleep and print time
        left.
        <br>`param seconds` int|float, how long sleep
        <br>`param verbose` boolean, print remaining time
        <br>`param check_per_sec` int|float, how often check time
        <br>`return` None
        """
        if seconds < 0:
            raise ValueError("sleep time must be non-negative")
        if verbose:
            cls._timer(seconds, check_per_sec)
        else:
            import time
            time.sleep(seconds)

    @classmethod
    def delta(cls, time_a, time_b):
        """
        <br>`param time_a` datetime.datetime time object|float of timestamp
        <br>`param time_b` datetime.datetime time object|float of timestamp
        <br>`return` difference between two timestamps
        """
        if time_a > time_b:
            time_a, time_b = time_b, time_a
        time_a = cls.timestamp_to_datetime(time_a)
        time_b = cls.timestamp_to_datetime(time_b)
        delta = time_b - time_a
        delta_combined = delta.seconds + delta.microseconds / 1E6
        return delta_combined

# datetime.datetime.now().strftime('some') todo implement
# Popen work with todo implement