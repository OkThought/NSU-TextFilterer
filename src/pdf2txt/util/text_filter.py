import re
import shutil
import tempfile

formula_regexp_str = r'(?:\s*[()\w\d, ]*\s*[\^\-+=<>≤≥*\/|])+\s*[,()\w\d]*'
# formula_sentence_regexp_str = r'(?:^|(?<=[.!?\n\r]).*)(?:([\'\"]).*\1)*' + formula_regexp_str + r'[^.!?\n\r]*\s*[!?.]?'

formula_regexp = re.compile(formula_regexp_str)
# formula_sentence_regexp = re.compile(formula_sentence_regexp_str)


def is_formula(text: str):
    return formula_regexp.fullmatch(text) is not None


def contains_formula(text: str):
    return formula_regexp.search(text) is not None


def is_formula_sentence(text: str):
    # return formula_sentence_regexp.fullmatch(text) is not None
    return False


def remove_formulas_from_file(filename: str):
    with tempfile.TemporaryFile() as tmp_fp:
        with open(filename, 'w+') as f:
            shutil.copyfileobj(f, tmp_fp)
            f.seek(0)
            f.truncate()
            for line in tmp_fp:
                if not contains_formula(line):
                    f.write(line)

