import unittest

from pdf2txt.util.text_filter import is_formula_sentence


class TextFilterTest(unittest.TestCase):
    def is_formula_test(self):
        self.assertTrue(is_formula_sentence("a+b"))
        self.assertTrue(is_formula_sentence("a-b"))
        self.assertTrue(is_formula_sentence("a*b"))
        self.assertTrue(is_formula_sentence("a/b"))
        self.assertTrue(is_formula_sentence("a>b"))
        self.assertTrue(is_formula_sentence("a<b"))
        self.assertTrue(is_formula_sentence("a≥b"))
        self.assertTrue(is_formula_sentence("a≤b"))
        self.assertTrue(is_formula_sentence("a>=b"))
        self.assertTrue(is_formula_sentence("a<=b"))
        self.assertTrue(is_formula_sentence("a=b"))
        self.assertTrue(is_formula_sentence("f(x)=ax+b"))
        self.assertTrue(is_formula_sentence("f (x, a, b, c) = a x^2 + b x + c"))


if __name__ == '__main__':
    unittest.main()
