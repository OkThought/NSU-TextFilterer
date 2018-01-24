#!/usr/bin/env python3
import string
import sys
import os

from util.filter_text import TextFilterer

DEFAULT_SENTENCE_DELIMITERS = '.!?'
DEFAULT_SKIP_CHARS = r'#@$\\`'
DEFAULT_OPERATION_CHARS = r'+=*<>≤≥|^'
DEFAULT_OPERAND_CHARS = r'_()\w'


def main(args=None):
    import argparse
    p = argparse.ArgumentParser()

    p.add_argument('src', nargs='?', default=None,
                   help='file to filter. By default stdin.')

    p.add_argument('dst', nargs='?', default=None,
                   help='filtered file. By default stdout or "<src_file_path>-filtered.<src_file_extension>" if src is '
                        'specified.')

    p.add_argument('--sentence-delimiters', default=DEFAULT_SENTENCE_DELIMITERS, nargs='*', metavar='char',
                   help='characters indicating sentence endings and beginnings. '
                        'By default: "{}"'.format(DEFAULT_SENTENCE_DELIMITERS))

    p.add_argument('--operation-chars', default=DEFAULT_OPERATION_CHARS, nargs='*', metavar='char',
                   help='characters of which math operations consist. '
                        'By default: {}'.format(DEFAULT_OPERATION_CHARS))

    p.add_argument('--keep-sentences-with-formulas', default=False, action='store_true',
                   help='when specified does not filter sentences with formulas.')

    p.add_argument('--skip-chars', default=DEFAULT_SKIP_CHARS, nargs='*', metavar='char',
                   help='characters not written to dst. '
                        'By default: "{}"'.format(DEFAULT_SKIP_CHARS))

    a = p.parse_args(args)

    if a.dst and a.dst == a.src or a.src and not a.dst:
        dir_path, name = os.path.split(a.src)
        name, extension = os.path.splitext(name)
        name = '%s-filtered%s' % (name, extension)
        a.dst = os.path.join(dir_path, name)

    if a.src and os.stat(a.src).st_size == 0:
        # src file is empty
        # create empty dst file
        if a.dst:
            open(a.dst, 'w').close()
        return

    src = dst = None
    try:
        src = open(a.src, 'r') if a.src else sys.stdin
        dst = open(a.dst, 'w') if a.dst else sys.stdout

        file_filterer = TextFilterer(
            src=src,
            dst=dst,
            sentence_delimiters=a.sentence_delimiters,
            formula_operation_chars=a.operation_chars,
            formula_operand_chars=DEFAULT_OPERAND_CHARS,
            remove_sentences_with_formulas=not a.keep_sentences_with_formulas,
            chars_to_remove=a.skip_chars)
        file_filterer.filter()
    finally:
        if src and src is not sys.stdin:
            src.close()
        if dst and dst is not sys.stdout:
            dst.close()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))