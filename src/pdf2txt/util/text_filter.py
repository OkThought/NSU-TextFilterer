import re
import shutil
import tempfile

from collections import Iterable

import os


def create_temporary_copy(src):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, src + '.tmp')
    shutil.copy2(src, temp_path)
    return temp_path


def remove_temporary_copy(temp_path):
    os.remove(temp_path)


class TextFilterer:

    def __init__(self, filter_formulas=True, chars_to_skip: Iterable = '', use_regex=True):
        self.filter_formulas = filter_formulas
        self.chars_to_skip = chars_to_skip
        self.use_regex = use_regex
        if use_regex:
            self.formula_regexp_str = r'(?:\s*[()\w\d, ]*\s*[\^\-+=<>≤≥*\/|])+\s*[,()\w\d]*'
            self.formula_regexp = re.compile(self.formula_regexp_str)
        else:
            # unsupported yet
            pass

    def is_formula(self, text: str):
        return self.formula_regexp.fullmatch(text) is not None

    def contains_formula(self, text: str):
        return self.formula_regexp.search(text) is not None

    def find_formula(self, text: str):
        match = self.formula_regexp.search(text)
        return match.pos, match.endpos

    @staticmethod
    def filter_chars(text: str, chars: Iterable):
        return ''.join(char for char in text if char not in chars)

    def filter_text(self, text: str):
        if self.filter_formulas and self.contains_formula(text):
            return ''
        if self.chars_to_skip:
            return self.filter_chars(text, self.chars_to_skip)

    def filter(self, src: str, dst: str = None):
        if dst is None:
            [dir, name] = os.path.split(src)
            dst = dir + "filtered-" + name

        with open(src) as src_file:
            with open(dst, 'w+') as dst_file:
                for line in src_file:
                    line = self.filter_text(text=line)
                    if line:
                        dst_file.write(line)