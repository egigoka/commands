#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with time
"""
__version__ = "0.1.6"


class Time:
    """Class to work with time
    """
    @staticmethod
    def _lp2(string, length=2):
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
        time = cls._lp2(time.year) + "." + cls._lp2(time.month) + "." + cls._lp2(time.day) + "_at_" + \
            cls._lp2(time.hour) + "." + cls._lp2(time.minute) + "." + cls._lp2(time.second) + "." + \
            cls._lp2(time.microsecond, 6)
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
                Print.rewrite("Timer for " + str(seconds) + " seconds. " + str(secs_left_int) + " left")
        Print.rewrite("")

    @classmethod
    def sleep(cls, seconds, quiet_small=False, check_per_sec=10):
        """Function to idle. If 'seconds more, than 1, running Time._timer. Otherwise run time.sleep and print time
        left.
        <br>`param seconds` int|float, how long sleep
        <br>`param quiet_small` boolean, suppress print for time len <= 1 second
        <br>`param check_per_sec` int|float, how often check time
        <br>`return` None
        """
        if seconds < 0:
            raise ValueError("sleep time must be non-negative")
        elif seconds >= 1:
            cls._timer(seconds, check_per_sec)
        else:
            if not quiet_small:
                print("sleeping", seconds)
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