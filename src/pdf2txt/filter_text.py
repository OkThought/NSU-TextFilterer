#!/usr/bin/env python

import fileinput
import string
import sys

from pdf2txt.util.text_filter import filter_text

symbols_to_filter = string.digits + string.punctuation


def main(args=None):
    for line in fileinput.input():
        print(filter_text(line, filter_formulas=True, symbols_to_filter=symbols_to_filter))


if __name__ == '__main__':
    sys.exit(main(sys.args))