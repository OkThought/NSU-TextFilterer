import re
import shutil
import tempfile

from collections import Iterable

formula_regexp_str = r'(?:\s*[()\w\d, ]*\s*[\^\-+=<>≤≥*\/|])+\s*[,()\w\d]*'
# formula_sentence_regexp_str = r'(?:^|(?<=[.!?\n\r]).*)(?:([\'\"]).*\1)*' + formula_regexp_str + r'[^.!?\n\r]*\s*[!?.]?'

formula_regexp = re.compile(formula_regexp_str)
# formula_sentence_regexp = re.compile(formula_sentence_regexp_str)


def is_formula(text: str):
    return formula_regexp.fullmatch(text) is not None


def contains_formula(text: str):
    return formula_regexp.search(text) is not None


def find_formula(text: str):
    match = formula_regexp.search(text)
    return match.pos, match.endpos


def is_formula_sentence(text: str):
    # return formula_sentence_regexp.fullmatch(text) is not None
    return False


def filter_symbols(text: str, symbols: Iterable):
    return ''.join(char for char in text if char not in symbols)


def filter_file(filename: str, filter_formulas=True, symbols_to_filter=''):
    with tempfile.TemporaryFile() as tmp_fp:
        with open(filename, 'w+') as f:
            shutil.copyfileobj(f, tmp_fp)
            f.seek(0)
            f.truncate()
            for line in tmp_fp:
                if filter_formulas and contains_formula(line):
                    continue
                if symbols_to_filter:
                    filter_symbols(line, symbols_to_filter)


