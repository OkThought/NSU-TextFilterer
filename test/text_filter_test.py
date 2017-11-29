import unittest

from pdf2txt.util.text_filter import is_formula


class TestTextFilter(unittest.TestCase):
    def test_is_formula(self):
        self.assertTrue(is_formula("a+b"))
        self.assertTrue(is_formula("a-b"))
        self.assertTrue(is_formula("a*b"))
        self.assertTrue(is_formula("a/b"))
        self.assertTrue(is_formula("a>b"))
        self.assertTrue(is_formula("a<b"))
        self.assertTrue(is_formula("a≥b"))
        self.assertTrue(is_formula("a≤b"))
        self.assertTrue(is_formula("a>=b"))
        self.assertTrue(is_formula("a<=b"))
        self.assertTrue(is_formula("a=b"))

    def test_is_formula_complex(self):
        self.assertTrue(is_formula("f(x)=ax+b"))
        self.assertTrue(is_formula("f (x, a, b, c) = a x^2 + b x + c"))


if __name__ == '__main__':
    unittest.main()
