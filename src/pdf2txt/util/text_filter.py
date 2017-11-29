import re
import shutil
import tempfile

import mmap

formula_regexp_str = r'(?:[()\w\d]*\s*[\^\-+=<>≤≥*\/|])+\s*[()\w\d]*'
formula_sentence_regexp_str = r'[^.!?\n\r]*' + formula_regexp_str + r'+\s*[()\w\d]*[^.!?\n\r]*\s*'

formula_regexp = re.compile(formula_regexp_str)
formula_sentence_regexp = re.compile(formula_sentence_regexp_str)


def is_formula(text: str):
    return formula_regexp.fullmatch(text) is not None


def is_formula_sentence(text: str):
    return formula_sentence_regexp.fullmatch(text) is not None


def remove_formulas_from_file(filename: str):
    with tempfile.TemporaryFile() as tmp_fp:
        with open(filename, 'w+') as f:
            shutil.copyfileobj(f, tmp_fp)
            f.seek(0)
            f.truncate()
            for line in tmp_fp:
                if not is_formula_sentence(line):
                    f.write(line)

