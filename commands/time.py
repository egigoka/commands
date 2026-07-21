#! python3
# -*- coding: utf-8 -*-
"""Module with time functions."""
from __future__ import annotations

from typing import TYPE_CHECKING
from .module import LazyModule, LazyProperty

__version__ = "1.2.5"

if TYPE_CHECKING:
    import datetime as datetime_module
    import time
    from typing import Any, Dict, List, Optional, Tuple, Union
    from .bench import Bench
    from .print import Print
    from .str import Str
else:
    Str = LazyProperty(".str", "Str")
    Print = LazyProperty(".print", "Print")
    Bench = LazyProperty(".bench", "Bench")
    datetime_module = LazyModule("datetime")
    time = LazyModule("time")


class Time:
    """Module with time functions."""

    def __getattribute__(self, name: str) -> Any:
        """Proxy selected attributes to classmethod helpers."""
        if name in {"delta", "to_timestamp"}:
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                dt = object.__getattribute__(self, "datetime")
                if name == "to_timestamp":
                    return self.__class__.datetime_to_timestamp(dt)
                if args:
                    return self.__class__.delta(dt, args[0])
                return self.__class__.delta(dt, dt)
            return _wrapper
        return object.__getattribute__(self, name)

    def __init__(self, datetime_object: Optional[datetime_module.datetime] = None) -> None:
        object.__setattr__(self, "datetime", datetime_object or datetime_module.datetime.now())

    @classmethod
    def __lp2(cls, string: Any, length: int = 2) -> str:
        """Pad a value with leading zeros."""
        return Str.leftpad(string, length, 0)

    @classmethod
    def stamp(cls) -> float:
        """Return the current Unix timestamp.

        <br>`return` float, timestamp
        """
        return time.time()

    @classmethod
    def datetime(
        cls,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        tzinfo: Optional[datetime_module.tzinfo] = None,
        fold: Optional[int] = None
    ) -> datetime_module.datetime:
        """Build a datetime from provided components."""
        now = datetime_module.datetime.now()
        args: Dict[str, Any] = {}
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

    @classmethod
    def timestamp_to_datetime(cls, timestamp: Union[float, int, str, datetime_module.datetime]) -> datetime_module.datetime:
        """Convert a timestamp to a datetime.

        <br>`param timestamp` float, timestamp
        <br>`return` datetime.datetime time object
        """
        if isinstance(timestamp, (str, int)):
            timestamp = float(timestamp)
        elif isinstance(timestamp, float):
            pass
        elif isinstance(timestamp, datetime_module.datetime):
            return timestamp
        else:
            raise TypeError(f"timestamp must be float, int or str, not {type(timestamp)}")
        return datetime_module.datetime.fromtimestamp(timestamp)

    @classmethod
    def datetime_to_timestamp(cls, datetime_object: Union[datetime_module.datetime, float]) -> float:
        """Convert a datetime to a timestamp.

        <br>`param datetime_object` datetime.datetime time object
        <br>`return` float, timestamp
        """
        if isinstance(datetime_object, float):
            return datetime_object
        return time.mktime(datetime_object.timetuple())

    @classmethod
    def dotted(cls, custom_time: Optional[Union[datetime_module.datetime, float]] = None) -> str:
        """Format time as dotted string.

        <br>`param custom_time` datetime.datetime time object|float of timestamp
        <br>`return` string with time in format "1999.12.31_at_12.59.59.999999"
        """
        if custom_time:
            time_obj = cls.timestamp_to_datetime(custom_time)
        else:
            time_obj = datetime_module.datetime.now()
        result = cls.__lp2(time_obj.year) + "." + cls.__lp2(time_obj.month) + "." + cls.__lp2(time_obj.day) + "_at_" + \
            cls.__lp2(time_obj.hour) + "." + cls.__lp2(time_obj.minute) + "." + cls.__lp2(time_obj.second) + "." + \
            cls.__lp2(time_obj.microsecond, 6)
        return result

    @classmethod
    def _timer(cls, seconds: float, check_per_sec: int = 10) -> None:
        """Idle and print remaining time (used in Time.sleep).

        <br>`param seconds` int|float, how long sleep
        <br>`param check_per_sec` int|float, how often check time
        <br>`return` None
        """
        benchmark = Bench()
        secs_second_var = int(seconds)
        while benchmark.get() < seconds:
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
    def sleep(cls, seconds: float, verbose: bool = False, check_per_sec: int = 10) -> None:
        """Sleep for a duration, optionally showing progress.

        If `seconds` is more than 1, run Time._timer. Otherwise, run time.sleep and print time left.
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
            time.sleep(seconds)

    @classmethod
    def delta(
        cls,
        time_a: Union[datetime_module.datetime, float, int],
        time_b: Optional[Union[datetime_module.datetime, float, int]] = None
    ) -> Union[float, datetime_module.timedelta]:
        """Get a time difference in seconds or as a timedelta.

        <br>`param time_a` datetime.datetime time object|float of timestamp
        <br>`param time_b` datetime.datetime time object|float of timestamp
        <br>`return` difference between two timestamps
        """
        if isinstance(time_a, (int, float)) and time_b is None:
            return datetime_module.timedelta(seconds=time_a)

        assert time_b is not None
        dt_a = cls.timestamp_to_datetime(time_a)
        dt_b = cls.timestamp_to_datetime(time_b)
        if dt_a > dt_b:
            dt_a, dt_b = dt_b, dt_a
        delta = dt_b - dt_a

        return delta.total_seconds()

    @classmethod
    def human_readable(cls, timedelta: Union[int, float, datetime_module.timedelta]) -> str:
        """Convert a timedelta to a human-readable string."""
        td: float
        if isinstance(timedelta, datetime_module.timedelta):
            td = timedelta.total_seconds()
        else:
            td = float(timedelta)

        units: List[Tuple[str, int]] = [('y', 31536000), ('m', 2592000), ('w', 604800), ('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
        units_len: Dict[str, int] = {'y': 4, 'm': 2, 'w': 2, 'd': 2, 'h': 2, 's': 2}

        total_seconds = int(td)
        microseconds = int((td - total_seconds) * 1000000)

        parts: List[str] = []

        for unit, factor in units:
            if total_seconds >= factor or parts:
                value, total_seconds = divmod(total_seconds, factor)
                zeros = 0
                if parts:
                    zeros = units_len[unit]
                parts.append(f"{str(value).zfill(zeros)}{unit}")

        if microseconds > 0:
            parts.append(f"{microseconds:06}ms")

        return " ".join(parts)

# datetime.datetime.now().strftime('some') todo implement
# Popen work with todo implement
