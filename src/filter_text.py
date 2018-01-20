#!/usr/bin/env python3
import string
import sys
import os

from util.filter_text import TextFilterer


def main(args=None):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('src', nargs='?', default=None,
                   help='file to filter. By default `stdin`')
    p.add_argument('dst', nargs='?', default=None,
                   help='filtered file. By default `stdout` or if src defined')
    p.add_argument('--keep-sentences-with-formulas', default=False, action='store_true',
                   help='when specified does not filter sentences with formulas')
    p.add_argument('--sentence-delimiters', default=['.'], nargs='*', metavar='char',
                   help='characters indicating sentence endings and beginnings')
    p.add_argument('--skip-chars', default=string.punctuation, nargs='*', metavar='char',
                   help='characters not written to dst')
    a = p.parse_args(args)

    if a.dst and a.dst == a.src or a.src and not a.dst:
        dir_path, name = os.path.split(a.src)
        name, extension = os.path.splitext(name)
        name = '%s-filtered%s' % (name, extension)
        a.dst = os.path.join(dir_path, name)

    if os.stat(a.src).st_size == 0:
        # src file is empty
        return

    with    open(a.src, 'r') if a.src else sys.stdin as _in, \
            open(a.dst, 'w') if a.dst else sys.stdout as _out:
        file_filterer = TextFilterer(_in, _out,
            remove_sentences_with_formulas=not a.keep_sentences_with_formulas,
            chars_to_skip=a.skip_chars, sentence_delimiters=a.sentence_delimiters)
        file_filterer.filter()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))