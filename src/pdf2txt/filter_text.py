#!/usr/bin/env python3

import fileinput
import string
import sys

# from util.text_filter import TextFilterer
from util.text_filter import TextFilterer

chars_to_skip = string.digits + string.punctuation


def main(args=None):
    file_filterer = TextFilterer(filter_formulas=True, chars_to_skip=chars_to_skip)
    if len(args) == 3:
        file_filterer.filter(args[1], args[2])
    else:
        file_filterer.filter(args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))