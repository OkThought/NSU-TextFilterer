import os
import re
import shutil
import tempfile
from collections import Iterable


def create_temporary_copy(src):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, src + '.tmp')
    shutil.copy2(src, temp_path)
    return temp_path


def remove_temporary_copy(temp_path):
    os.remove(temp_path)


class TextFilterer:

    def __init__(self, src, dst, filter_sentences_with_formulas=True, chars_to_skip: Iterable = '', use_regex=False,
                 sentence_delimiters=None):
        self.src = src
        self.dst = dst
        self.filter_sentences_with_formulas = filter_sentences_with_formulas
        self.chars_to_skip = chars_to_skip
        self.use_regex = use_regex
        if use_regex:
            self.formula_regexp_str = r'(?:\s*[()\w\d, ]*\s*[\^\-+=<>≤≥*\/|])+\s*[,()\w\d]*'
            self.formula_regexp = re.compile(self.formula_regexp_str)
        else:
            if sentence_delimiters is None:
                sentence_delimiters = ['.']
            self.sentence_delimiters = sentence_delimiters

    def is_formula(self, text: str):
        return self.formula_regexp.fullmatch(text) is not None

    def contains_formula(self, text: str):
        if self.use_regex:
            return self.formula_regexp.search(text) is not None
        # TODO: implement non-regex

    def find_formula(self, text: str):
        match = self.formula_regexp.search(text)
        return match.pos, match.endpos

    @staticmethod
    def filter_chars(text: str, restricted_chars: Iterable):
        return ''.join(char for char in text if char not in restricted_chars)

    def filter_text(self, text: str):
        if text is None: return None
        if self.filter_sentences_with_formulas and self.contains_formula(text):
            return ''
        if self.chars_to_skip:
            return self.filter_chars(text, self.chars_to_skip)

    def find_one_of(self, values, direction=1):
        if not values:
            raise RuntimeError("values set either None or empty")
        if direction not in [-1, 1]:
            raise RuntimeError("direction must be either -1 or 1, found: %d" % direction)
        pos = self.pos + 1
        src = self.src
        while pos < len(src) and src[pos] not in values:
            pos += direction
        return pos

    def filter(self):
        if self.use_regex:
            for line in self.src:
                line = self.filter_text(text=line)
                if line:
                    self.dst.write(line)
            return
        for sentence in self:
            self.dst.write(sentence)

    def next_sentence(self):
        if self.use_regex: return self.src.readLine()
        # TODO: implement

    def __iter__(self):
        self.pos = 0
        self.sentence_start = 0
        self.sentence_end = -1
        return self

    def __next__(self):
        return self.filter_text(self.next_sentence())



