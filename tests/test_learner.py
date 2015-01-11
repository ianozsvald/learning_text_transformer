import unittest
from learning_text_transformer import learner3 as learner
from learning_text_transformer import transforms


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
        transform_searcher = learner.TransformSearcher()
        chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        string_form_of_transforms = repr(chosen_transformations)
        self.assertIn("TransformRemoveWords", string_form_of_transforms)
        self.assertIn("TransformSpokenWordsToNumbers", string_form_of_transforms)
        self.assertEqual(best_score, 0)
