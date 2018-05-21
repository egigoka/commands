#! python3
# -*- coding: utf-8 -*-
# http://python.su/forum/topic/15531/?page=1#post-93316
__version__ = "0.2.2"


def get_Bench(start=False):  # return class with those functions:
    class Bench(object):  # dir ignore
        import datetime
        time_start = datetime.datetime.now()
        time_end = None
        quiet = False  # d argument for disable print to terminal               bnl1
        prefix = "Bench runned in"  # d what have been done, will print if      bnl1
        fraction_digits = 3
        # d "quiet" variable of class is False

        @classmethod
        def start(cls):  # set time of begin to now
            import datetime
            cls.time_start = datetime.datetime.now()

        @classmethod
        def get(cls):  # dir ignore
            import datetime
            cls.time_end = datetime.datetime.now()
            def delta(time_a, time_b):
                delta = time_b - time_a
                return delta.seconds + delta.microseconds / 1E6
            return delta(cls.time_start, cls.time_end)

        @classmethod
        def end(cls, prefix_string=None, quiet_if_zero=False, start_immideately=False):  # return delta between start and end
            delta = cls.get()
            cls.start()
            if prefix_string:
                cls.prefix = prefix_string
            if not cls.quiet:
                #print(not quiet_if_zero, str(round(delta, cls.fraction_digits)), (str(round(delta, cls.fraction_digits)) != "0.0"), (not quiet_if_zero) and (str(round(delta, cls.fraction_digits)) != "0.0"))
                if (not quiet_if_zero) or (str(round(delta, cls.fraction_digits)) != "0.0"):
                    try:
                        from termcolor import cprint
                        import colorama
                        colorama.init()
                        cprint(cls.prefix + " " + str(round(delta, cls.fraction_digits)) + " seconds", "grey", "on_white")
                    except TypeError:
                        print(cls.prefix + " " + str(round(delta, cls.fraction_digits)) + " seconds")
                    except AttributeError:
                        print(cls.prefix + " " + str(round(delta, cls.fraction_digits)) + " seconds")
            return delta
    return Bench
