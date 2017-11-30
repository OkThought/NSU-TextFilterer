import unittest

from pdf2txt.util.text_filter import is_formula, is_formula_sentence, filter_symbols


class TestTextFilter(unittest.TestCase):
    def setUp(self):
        self.empty_formulas = ['', ' ', '    ', '\t', '\n', '\r', '\n\n', '\n\r\t\t\r\n']
        self.simple_formulas = ['a+b', 'a-b', 'a*b', 'a/b', 'a>b', 'a<b', 'a≥b', 'a≤b', 'a>=b', 'a<=b', 'a=b']
        self.complex_formulas = ['f(x)=ax+b', 'f (x, a, b, c) = a x^2 + b x + c', '-a+b']
        # self.sentence_endings = ['.', '!', '?', r'\n', r'\n\r', r'\r']
        self.sentence_endings = []
        self.phrases = ['Some text', 'Word', 'word', 'And he said: \"Stop it!\"', 'this was k to the power of n']
        # self.sentences = [phrase + ending for phrase in self.phrases for ending in self.sentence_endings]
        self.sentences = []
        self.possible_text_formula_separators = [': ', ':', ' ', '\t', ',']

    def test_is_formula_empty(self):
        for empty_formula in self.empty_formulas:
            self.assertFalse(is_formula(empty_formula))

    def test_is_formula(self):
        for formula in self.simple_formulas:
            self.assertTrue(is_formula(formula))

    def test_is_formula_complex(self):
        for formula in self.complex_formulas:
            self.assertTrue(is_formula(formula))

    @unittest.skip
    def test_is_formula_sentence_empty(self):
        for empty_formula in self.empty_formulas:
            self.assertFalse(is_formula_sentence(empty_formula))

    @unittest.skip
    def test_is_formula_sentence_on_formulas(self):
        for formula in self.simple_formulas + self.complex_formulas:
            self.assertTrue(is_formula_sentence(formula))

    @unittest.skip
    def test_is_formula_sentence(self):
        for sentence in self.sentences:
            self.assertFalse(is_formula_sentence(sentence))

        for phrase in self.phrases:
            for formula in self.simple_formulas + self.complex_formulas:
                for separator in self.possible_text_formula_separators:
                    for ending in self.sentence_endings:
                        formula_sentence = phrase + separator + formula + ending
                        repr(formula_sentence)
                        self.assertTrue(is_formula_sentence(formula_sentence), formula_sentence)

    def test_filter_symbols(self):
        self.assertEqual('some text', filter_symbols('s!o@m#e$ %t^e&x*t()_+-', '!@#$%^&*()_+-'))

if __name__ == '__main__':
    unittest.main()
