#! python3
# -*- coding: utf-8 -*-
"""Internal module to work with lists
"""
__version__ = "0.0.7"


class List:
    """Class to work with lists
    """
    @staticmethod
    def flatterize(input_list):
        """Remove nesting from lists.
        :param input_list: list
        :return: list with all contents of input list but without nesting
        """
        import copy
        if not isinstance(input_list, (list, tuple)):
            raise TypeError("object of type '" + str(type(input_list)) + "' can't be flatterized")
        output_list = copy.deepcopy(list(input_list))
        cnt = 0
        for object_ in output_list:
            if not isinstance(object_, (str, int)):
                output_list.pop(cnt)
                for item in reversed(object_):
                    output_list.insert(cnt, item)
            cnt += 1
        return output_list

    @staticmethod
    def split_every(list_input, count):
        """Split list to lists with N elements
        :param list_input: list
        :param count: int with N
        :return: list of lists
        """
        count = int(count)
        output_lists = [list_input[x:x+count] for x in range(0, len(list_input), count)]
        # https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
        return output_lists  # todo отдебажить пограничные моменты