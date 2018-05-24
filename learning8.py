#! python3
# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, missing-docstring, too-many-nested-blocks,
from .os8 import *
from .print8 import *
from .str8 import *
from .random8 import *
from .int8 import *
__version__ = "1.0.3"


def bubblesort(list_, quiet=True):
    import copy
    list_ = copy.deepcopy(list_)
    is_sorted = False
    if not quiet:
        maxcnt = 0
        lenlist = len(list_)
    while not is_sorted:
        cnt = 0
        while True:
            try:
                if list_[cnt] > list_[cnt + 1]:
                    temp_var = list_[cnt]
                    list_[cnt] = list_[cnt + 1]
                    list_[cnt + 1] = temp_var
                    if not quiet:
                        if cnt > maxcnt:
                            maxcnt = cnt
                            output_string = Str.leftpad(str(maxcnt), len(str(lenlist)))+"/"+str(lenlist)
                            if OS.macos:
                                output_string = " " + output_string
                            Print.rewrite(output_string)
                    break
                cnt += 1
            except IndexError:  # значит, прошлись по всему списку и всё ок
                is_sorted = True
                break
    return list_


def bigdigits(digits):
    def digits_init(height=False):
        zero = ["   ###   ",
                "  #   #  ",
                " #     # ",
                "#       #",
                " #     # ",
                "  #   #  ",
                "   ###   ", ]
        one = ["    #    ",
               "   ##    ",
               "  # #    ",
               "    #    ",
               "    #    ",
               "    #    ",
               " ####### ", ]
        two = [" ####### ",
               "#       #",
               "        #",
               " ####### ",
               "#        ",
               "#        ",
               "#########", ]
        three = [" ####### ",
                 "#       #",
                 "        #",
                 "     ### ",
                 "        #",
                 "#       #",
                 " ####### ", ]
        four = ["#       #",
                "#       #",
                "#       #",
                "#########",
                "        #",
                "        #",
                "        #", ]
        five = ["#########",
                "#        ",
                "#        ",
                "######## ",
                "        #",
                "#       #",
                " ####### ", ]
        six = [" ####### ",
               "#       #",
               "#        ",
               "######## ",
               "#       #",
               "#       #",
               " ####### ", ]
        seven = ["#########",
                 "#       #",
                 "      ## ",
                 "    ##   ",
                 "  ##     ",
                 " #       ",
                 "#        ", ]
        eight = [" ####### ",
                 "#       #",
                 "#       #",
                 " ####### ",
                 "#       #",
                 "#       #",
                 " ####### ", ]
        nine = [" ####### ",
                "#       #",
                "#       #",
                " ########",
                "        #",
                "#       #",
                " ####### ", ]
        digits = [zero, one, two, three, four, five, six, seven, eight, nine]
        height_int = len(zero)
        if height:
            return height_int
        return digits
    digits = digits_init()
    column = 0
    while column < digits_init(height=True):
        line = ""
        digits = str(digits)
        for digit in digits:
            # try:
            digit = int(digit)
            line = line + digits[digit][column].replace("#", str(digit)) + " "
        print(line)
        column += 1

def simple_calc_page65():
    list_ = []
    try:
        while True:
            list_.append(Str.input_int(debug=True))
    except ValueError:
        mean = 0
        for item in list_:
            mean += item
        mean /= len(list_)
        print("numbers:", list_)
        print("count =", len(list_), "lowest =", min(list_), "highest =", max(list_), "mean =", mean)

def simple_calc_advanced_page66():
    list_ = []
    try:
        while True:
            list_.append(Str.input_int(debug=True))
    except ValueError:
        if list_ == 0:
            print("no input")
        else:
            mean = 0
            for item in list_:
                mean += item
            mean /= len(list_)
            if len(list_) % 2 == 1:
                median = list_[int(0.5+((len(list_)-1)/2))]  # средний элемент списка
            else:
                median = (list_[int(len(list_)/2)]+list_[int(len(list_)/2)-1])/2
                # среднеарифметическое среди двух средних элементов
            print("numbers:", list_)
            print("count =", len(list_),
                  "lowest =", min(list_),
                  "highest =", max(list_),
                  "mean =", mean,
                  "median =", median)

def awful_poetry_page65(sentences=5):
    articles = ["a", "the"]
    pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their'] + articles
    pronouns_plural = ['mine', 'yours', 'his', 'hers', 'its', 'ours', 'its', 'ours', 'yours', 'theirs'] + articles
    pronouns = [pronouns, pronouns_plural]
    nouns = ["cat", "women", "men", "dog", "cluster", "Sonic the Hedgehog", "queen", "breast"]
    nouns_multiple = ["cats", "women", "men", "dogs", "clusters", "Sonics the Hedgehogs", "queens", "breasts"]
    nouns = [nouns, nouns_multiple]
    verbs = ["jumped", "fucked", "fucks", "sang", "ran", "clusteryfied", "died"]
    adverbs = ["as fuck", "loudly", "well", "badly", "quetly"]

    for _ in Int.from_to(1, sentences):
        multiple = Random.integer(0, 1)
        print(pronouns[multiple][Random.integer(0, len(pronouns[multiple])-1)].capitalize(), end=" ")
        print(nouns[multiple][Random.integer(0, len(nouns[multiple]) - 1)], end=" ")
        print(verbs[Random.integer(0, len(verbs)-1)], end=" ")
        print(adverbs[Random.integer(0, len(adverbs) - 1)], end="")
        print(".", end=" ")
    print()
