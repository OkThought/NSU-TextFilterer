import filecmp
import unittest

import os

import shutil

import filter_text


class TestFilterText(unittest.TestCase):
    test_files_dir = 'cases/input'
    expected_files_dir = 'cases/expected'
    result_files_dir = 'cases/output'
    keep_results = True

    def setUp(self):
        # print(os.listdir("cases"))
        if not os.path.isdir(TestFilterText.result_files_dir):
            os.mkdir(TestFilterText.result_files_dir)

    def test_on_files(self):
        test_file_names = os.listdir(TestFilterText.test_files_dir)
        for test_file_name in test_file_names:
            t = os.path.join(self.test_files_dir, test_file_name)
            r = os.path.join(self.result_files_dir, test_file_name)
            e = os.path.join(self.expected_files_dir, test_file_name)

            filter_text.main([t, r])
            self.assertTrue(filecmp.cmp(r, e, shallow=False), r + " ≠ " + e)

    def tearDown(self):
        if not self.keep_results and os.path.isdir(TestFilterText.result_files_dir):
            shutil.rmtree(TestFilterText.result_files_dir)


if __name__ == '__main__':
    unittest.main()
