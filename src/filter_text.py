#!/usr/bin/env python3
import string
import sys

from util.text_filter import TextFilterer


def main(args=None):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('src', nargs='?', default=None,
                   help='file to filter. By default `stdin`')
    p.add_argument('dst', nargs='?', default=None,
                   help='filtered file. By default `stdout` or if src defined')
    p.add_argument('--no-mmap', default=True, action='store_false',
                   help='disable mmap for the files')
    p.add_argument('--keep-formulas', default=False, action='store_true',
                   help='when specified does not filter sentences with formulas')
    p.add_argument('--sentence-delimiters', default=['.'], nargs='*', metavar='char',
                   help='characters indicating sentence endings and beginnings')
    p.add_argument('--skip-chars', default=string.punctuation, nargs='*', metavar='char',
                   help='characters not written to dst')
    a = p.parse_args(args)

    if a.dst and a.dst == a.src or a.src and not a.dst:
        import os
        dir_path, name = os.path.split(a.src)
        if dir_path and dir_path[-1] != os.pathsep:
            dir_path += os.pathsep
        name, extension = os.path.splitext(name)
        a.dst = '%s%s-filtered%s' % (dir, name, extension)

    print(a)
    with open(a.src, 'r') if a.src else sys.stdin as src, open(a.dst, 'w') if a.dst else sys.stdout as dst:
        if not a.no_mmap:
            import mmap
            src = mmap.mmap(fileno=src.fileno(), length=0)
            dst = mmap.mmap(fileno=dst.fileno(), length=0)
        file_filterer = TextFilterer(src, dst,
                                     filter_sentences_with_formulas=not a.keep_formulas,
                                     chars_to_skip=a.skip_chars,
                                     )
        file_filterer.filter(src, dst)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))