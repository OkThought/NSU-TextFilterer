import unittest

from pdf2txt.util.text_filter import TextFilterer


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
        self.text_filterer = TextFilterer()

    def test_is_formula_empty(self):
        for empty_formula in self.empty_formulas:
            self.assertFalse(self.text_filterer.is_formula(empty_formula))

    def test_is_formula(self):
        for formula in self.simple_formulas:
            self.assertTrue(self.text_filterer.is_formula(formula))

    def test_is_formula_complex(self):
        for formula in self.complex_formulas:
            self.assertTrue(self.text_filterer.is_formula(formula))

    def test_filter_symbols(self):
        self.assertEqual('some text', self.text_filterer.filter_chars('s!o@m#e$ %t^e&x*t()_+-', '!@#$%^&*()_+-'))

    def test_filter_text(self):
        self.assertEqual('', self.text_filterer.filter_text('First Axiom of Trigonometry: syn^2(x) + cos^2(x) = 1'))
        line = 'Clear text without special symbols like '
        garbage = '!@#$%^&*()'
        line_with_garbage = line + garbage
        self.assertEqual(line, self.text_filterer.filter_text(line_with_garbage))


if __name__ == '__main__':
    unittest.main()
