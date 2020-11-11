#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with lists
"""
__version__ = "0.10.2"


class List:
    """Class to work with lists
    """
    @staticmethod
    def flatterize(input_list):
        """Remove nesting from lists.
        <br>`param input_list` list
        <br>`return` list with all contents of input list but without nesting
        """
        import copy
        if not isinstance(input_list, (list, tuple)):
            raise TypeError("object of type '" + str(type(input_list)) + "' can't be flatterized")
        output_list = copy.deepcopy(list(input_list))
        cnt = 0
        for object_ in output_list:
            if not isinstance(object_, (str, int, float)):
                output_list.pop(cnt)
                for item in reversed(object_):
                    output_list.insert(cnt, item)
            cnt += 1
        return output_list

    @staticmethod
    def split_every(list_input, count):
        """Split list to lists with N elements
        <br>`param list_input` list
        <br>`param count` int with N
        <br>`return` list of lists
        """
        count = int(count)
        if count == 0:
            return [[list_input[x]] for x in range(0, len(list_input))]
        elif count > len(list_input):
            return [list_input, ]
        output_lists = [list_input[x:x+count] for x in range(0, len(list_input), count)]
        # https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
        return output_lists  # todo отдебажить пограничные моменты

    @staticmethod
    def wildcard_search(list_input, regexp):
        """Search list shell-like
        <br>`param list_input` list
        <br>`param regexp` string with shell-like wildcards` ? for one character or * for multiple characters.
        <br>`return` list of result of search
        """
        import fnmatch
        return fnmatch.filter(list_input, regexp)

    @staticmethod
    def replace_string(list, old_string, new_string):
        return [str(string).replace(old_string, new_string) for string in list]

    @staticmethod
    def apply_lambda_to_all_elements(list, function):
        return [function(string) for string in list]

    @classmethod
    def to_strings(cls, list):
        return cls.apply_lambda_to_all_elements(list, str)

    @staticmethod
    def remove_duplicates(source_list, preserve_order=True):
        if preserve_order:
            from collections import OrderedDict
            return list(OrderedDict((x, True) for x in source_list).keys())
        else:
            return list(set(source_list))

    @staticmethod
    def most_common(list, count):
        import collections
        c = collections.Counter(list)
        return c.most_common(count)

    @staticmethod
    def shuffle(list):
        import random
        import copy
        copy_list = copy.deepcopy(list)
        random.shuffle(copy_list)
        return copy_list

    @staticmethod
    def remove_empty_strings(list_: list):
        list_new = list_.copy()
        for cnt, item in enumerate(list_new):
            if item == "":
                list_new.pop(cnt)
        return list_new

    @staticmethod
    def itemgetter_with_casting(item, *items, cast_to):
        if not items:
            def func(obj):
                for type_to in cast_to:
                    try:
                        return type_to(obj[item])
                    except:
                        pass
                return obj[item]
        else:
            items = (item,) + items

            def func(obj):
                new_list = []
                for i in items:
                    added = False
                    for type_to in cast_to:
                        try:
                            new_list.append(type_to(obj[i]))
                            added = True
                            break
                        except:
                            pass
                    if not added:
                        new_list.append(obj[i])
                return tuple(new_list)
        return func

    @classmethod
    def sort_by(cls, list_input: list, *sort_keys, cast_to=()) -> list:
        return sorted(list_input, key=cls.itemgetter_with_casting(*sort_keys, cast_to=cast_to))

    @staticmethod
    def enum_by(list_input: list, *enum_keys, cast_to=()) -> dict:
        from operator import itemgetter
        new_dict = {}
        for value in list_input:
            itemgetter_current = itemgetter(*enum_keys)
            key = itemgetter_current(value)

            for type_to in cast_to:
                try:
                    value = type_to(value)
                    break
                except:
                    pass

            new_dict[key] = value
        return new_dict