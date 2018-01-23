import os
import re
import shutil
import string


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
        "«": "»",
        '(': ')',
        '[': ']',
        '{': '}',
        '`': '`',
    }

    DEFAULT_OPERATION_CHARS = r'[\^\+=<>≤≥*\/|]'
    DEFAULT_OPERAND_CHARS = r'[_()\w]'

    def __init__(self, src, dst, sentence_delimiters=None, chars_to_remove: str=None,
                 remove_sentences_with_formulas=True, formula_operation_chars: str=None,
                 formula_operand_chars: str=None):
        self.reader = src
        self.writer = dst

        self.sentence_delimiters = sentence_delimiters if sentence_delimiters else ['.']
        self.chars_to_remove = chars_to_remove

        self.filter_formulas = remove_sentences_with_formulas
        if remove_sentences_with_formulas:

            if formula_operand_chars is None:
                formula_operand_chars = TextFilterer.DEFAULT_OPERAND_CHARS
            self.operand_chars = formula_operand_chars

            if formula_operation_chars is None:
                formula_operation_chars = TextFilterer.DEFAULT_OPERATION_CHARS
            self.operation_chars = formula_operation_chars

            self.formula_regexp_str = r'(?:\s*{operand}+\s*{operation})+\s*{operand}+'.format(
                operand=self.operand_chars,
                operation=self.operation_chars)

            self.formula_regexp = re.compile(self.formula_regexp_str, flags=re.UNICODE)

        self.sentence_contains_operation_chars = False
        self.eof = False

    def is_formula(self, text: str):
        return self.formula_regexp.fullmatch(text) is not None

    def contains_formula(self, text: str):
        return self.formula_regexp.search(text) is not None

    def find_formula(self, text: str):
        match = self.formula_regexp.search(text)
        return match.pos, match.endpos

    def filter_sentence(self, sentence: str):
        if sentence is None:
            return None
        if self.filter_formulas and self.sentence_contains_operation_chars and self.contains_formula(sentence):
            return ''
        return sentence

    def filter(self):
        for sentence in self:
            self.writer.write(sentence)

    def read_sentence(self, escape_sequence_map=None):
        if escape_sequence_map is None:
            escape_sequence_map = TextFilterer.DEFAULT_ESCAPE_SEQUENCE_MAP
        self.sentence_contains_operation_chars = False
        sentence = ''
        escape = []
        while True:
            c = self.reader.read(1)

            if not c:
                # eof
                self.eof = True
                return sentence

            if c in self.operation_chars:
                self.sentence_contains_operation_chars = True

            if c in self.sentence_delimiters and not escape:
                sentence += c  # keep delimiter in sentence
                return sentence

            if escape and (escape[-1], c) in escape_sequence_map:
                escape.pop()
            elif c in escape_sequence_map.keys():
                escape.append(c)

            if not c in self.chars_to_remove:
                sentence += c

    def next_sentence(self):
        if self.eof:
            raise StopIteration
        sentence = self.read_sentence()
        if sentence is None:
            raise StopIteration
        return sentence

    def __iter__(self):
        return self

    def __next__(self):
        return self.filter_sentence(self.next_sentence())
