import unittest
import pytest
from learning_text_transformer import learner3 as learner
from learning_text_transformer import transforms


import time
def t1():
    time.sleep(1)


class Test(unittest.TestCase):
    def test1(self):
        #input_strings = ["some 33K"]
        #output_strings = ["33000"]
        #input_strings = ["some 30K"]
        input_strings = ["thirty three thousand Ltd"]
        output_strings = ["33000"]
        ts = transforms.get_transforms(input_strings, output_strings)
        #ts = transforms.TransformExtractNumber.factory(input_strings, output_strings) + transforms.TransformExpandK.factory(input_strings, output_strings) + transforms.TransformStrip.factory(input_strings, output_strings)
        #ts = ts[:3]
        print(ts)
        examples_to_learn_from = [(input_strings[0], output_strings[0])]
        transform_searcher = learner.get_transform_searcher()
        chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        string_form_of_transforms = repr(chosen_transformations)
        self.assertIn("TransformRemoveWords", string_form_of_transforms)
        self.assertIn("TransformSpokenWordsToNumbers", string_form_of_transforms)
        self.assertEqual(best_score, 0)

    @pytest.mark.timeout(1)
    def test_timeout(self):
        """Do something that's not possible to solve, check we timeout during the search"""
        # Strings that cannot be correctly converted
        input_strings = ["£34866 P.A.", "£48260 P.A.", "60000.00", "60K", "45000", "£60K", "45000"]
        output_strings = ["34866", "48260", "60000", "60000", "4500X", "6000", "45000"]
        examples_to_learn_from = zip(input_strings, output_strings)
        # pytest is set to timeout after 1s, we'll set timeout=0.5s so our
        # search exits before this test times out
        transform_searcher = learner.get_transform_searcher(timeout=0.5)
        chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        print(chosen_transformations)
        self.assertLess(best_score, 1)


    def test_check_no_transforms_means_noop(self):
        input_strings = ["x"]
        output_strings = ["x"]
        ts = transforms.get_transforms(input_strings, output_strings)
        print(ts)
        examples_to_learn_from = [(input_strings[0], output_strings[0])]
        transform_searcher = learner.get_transform_searcher()
        chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        print(chosen_transformations, best_score)
        self.assertEqual(len(chosen_transformations), 0)
        self.assertEqual(best_score, 0)
