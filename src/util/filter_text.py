import os
import re
import shutil
from collections import Sequence


def create_temporary_copy(src):
    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, src + '.tmp')
    shutil.copy2(src, temp_path)
    return temp_path


def remove_temporary_copy(temp_path):
    os.remove(temp_path)


class TextFilterer:
    DEFAULT_ESCAPE_SEQUENCE_MAP = {
        '"': '"',
        "'": "'",
        '(': ')',
        '[': ']',
        '{': '}',
        '`': '`',
    }

    def __init__(self, src, dst, remove_sentences_with_formulas=True, chars_to_skip: Sequence = '',
                 sentence_delimiters=None):
        self.reader = src
        self.writer = dst
        self.remove_sentences_with_formulas = remove_sentences_with_formulas
        self.chars_to_skip = chars_to_skip
        self.trans_table = str.maketrans(dict.fromkeys(chars_to_skip))
        self.formula_regexp_str = r'(?:\s*[()\w\d, ]*\s*[\^\-+=<>≤≥*\/|])+\s*[,()\w\d]*'
        self.formula_regexp = re.compile(self.formula_regexp_str)
        self.sentence_delimiters = sentence_delimiters if sentence_delimiters else ['.']
        self.eof = False

    def is_formula(self, text: str):
        return self.formula_regexp.fullmatch(text) is not None

    def contains_formula(self, text: str):
        return self.formula_regexp.search(text) is not None

    def find_formula(self, text: str):
        match = self.formula_regexp.search(text)
        return match.pos, match.endpos

    def filter_chars(self, text: str):
        return text.translate(self.trans_table)

    def filter_sentence(self, sentence: str):
        if sentence is None:
            return None
        if self.remove_sentences_with_formulas and self.contains_formula(sentence):
            return ''
        if self.chars_to_skip:
            return self.filter_chars(sentence)

    def filter(self):
        for sentence in self:
            self.writer.write(sentence)

    def read_sentence(self, escape_sequence_map=None):
        if escape_sequence_map is None:
            escape_sequence_map = TextFilterer.DEFAULT_ESCAPE_SEQUENCE_MAP
        sentence = ''
        escape = []
        while True:
            c = self.reader.read(1)
            if not c:
                # eof
                self.eof = True
                return sentence
            if c in self.sentence_delimiters and not escape:
                sentence += c  # keep delimiter in sentence
                return sentence
            if c in escape_sequence_map.keys():
                if escape and escape_sequence_map[c] == escape[-1]:
                    escape.pop()
                else:
                    escape.append(c)
            elif escape and (escape[-1], c) in escape_sequence_map:
                escape.pop()
            sentence += c

    def next_sentence(self):
        if self.eof:
            raise StopIteration
        sentence = self.read_sentence()
        if sentence is None:
            raise StopIteration
        return sentence

    def __iter__(self):
        self.pos = -1
        self.sentence_start = 0
        self.sentence_end = -1
        return self

    def __next__(self):
        return self.filter_sentence(self.next_sentence())
