"""Some tests"""
import unittest
import json
from learning_text_transformer import transforms
from learning_text_transformer import learner3 as learner


EMPTY_STRING = ""
# most items are (inp, expected_result) and t.apply(inp)->res
ITEM1 = ("30000.00", "30000")
ITEM2 = ("30K", "30000")
ITEM3 = ("blah 40 blah", "40")
ITEM4 = ("forty four", "44")
ITEM5 = ("thirty-three thousand", "33000")
ITEM6 = ("schÃ¶n", "schön")
ITEM7 = ("société", "societe")
ITEM8 = ("Mixed Case Ltd", "mixed case")

SERIALISED_REMOVEDOT00 = ('TransformRemoveDot00', {})
SERIALISED_UNKNOWN_CLASS = ('BlahBlah', {})


WORDS_TO_REMOVE = ("this thing ltd", "this thing ", ["ltd"])
# spoken word converter breaks on:
# "forty four hundred" -> "40400"
# empty input string


class TestSerialisation(unittest.TestCase):
    def setUp(self):
        self.serialiser = transforms.Serialisation()

    def test_unknown_class(self):
        """This class doesn't exist, check it throws a ValueError"""
        transform_name, parameters = SERIALISED_UNKNOWN_CLASS
        with self.assertRaises(ValueError):
            self.serialiser._deserialise_transform(transform_name, parameters)

    def test_removedot00(self):
        t = transforms.TransformRemoveDot00()
        self.assertEqual(t.serialise(), SERIALISED_REMOVEDOT00)

        transform_name, parameters = SERIALISED_REMOVEDOT00
        deserialised_t = self.serialiser._deserialise_transform(transform_name, parameters)
        self.assertEqual(deserialised_t.__class__, t.__class__)

    def test_remove_words(self):
        """Check we can serialise and deserialise RemoveWords with parameters"""
        t = transforms.TransformRemoveWords()
        inp, expected_res, terms = WORDS_TO_REMOVE
        t.configure(terms=terms)
        self.assertEqual(t.terms, "ltd")
        res = t.apply(inp)
        self.assertEqual(res, expected_res)

        transform_name, parameters = t.serialise()
        deserialised_t = self.serialiser._deserialise_transform(transform_name, parameters)
        self.assertEqual(deserialised_t.terms, "ltd")
        self.assertEqual(deserialised_t.__class__, t.__class__)
        deserialised_t_res = deserialised_t.apply(inp)
        self.assertEqual(deserialised_t_res, res)

    def test_serialiser_sequence(self):
        """Serialise 3 items, then deserialise, check they work as expected"""
        # NOTE this is oddly hardcoded, probably this can be improved?
        t1 = transforms.TransformRemoveWords.factory(["Ltd"], [""])
        t2 = transforms.TransformLowercase.factory("", "")
        t3 = transforms.TransformStrip.factory("", "")
        ts = t1 + t2 + t3
        transform_searcher = learner.get_transform_searcher()
        ts_output, transform_always_made_changes = transform_searcher.apply_transforms(ts, ITEM8[0])
        self.assertEqual(ts_output, ITEM8[1])

        serialised_raw = self.serialiser.serialise(ts)
        self.assertGreater(len(serialised_raw), 0)  # assume we have some bytes

        deserialised_ts = self.serialiser.deserialise(serialised_raw)
        deserialised_ts_output, transform_always_made_changes = transform_searcher.apply_transforms(deserialised_ts, ITEM8[0])
        self.assertEqual(deserialised_ts_output, ITEM8[1])


class TestSearchAndSerialise(unittest.TestCase):
    """Run the full process of searching for a transform sequence, serialise, deserialise"""
    def test_search(self):
        # take a simple input/output sequence, search for pattern
        examples_to_learn_from = [ITEM8]
        transform_searcher = learner.get_transform_searcher()
        chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        self.assertEqual(best_score, 0.0)

        # serialise the result
        serialisation = transforms.Serialisation()
        serialised_json = serialisation.serialise(chosen_transformations)

        # deserialise
        ts = serialisation.deserialise(serialised_json)

        # test on the same input, confirm same output
        result, transform_always_made_changes = transform_searcher.apply_transforms(ts, ITEM8[0])
        self.assertEqual(result, ITEM8[1])


class TestGetTransformations(unittest.TestCase):
    def setUp(self):
        self.expected_nbr_transforms = 7  # NOTE this will change when Transforms change

    def test_count_expected_transforms(self):
        input_strings, output_strings = [], []
        all_transforms = transforms.get_transforms(input_strings, output_strings)
        self.assertEqual(len(all_transforms), self.expected_nbr_transforms)

    def test_count_expected_transforms_with_basic_input_data(self):
        input_strings, output_strings = ["a b", "a c"], ["A B", "A C"]
        all_transforms = transforms.get_transforms(input_strings, output_strings)
        nbr_extra_transforms_expected = 3  # due to RemoveWords on a, b, c
        self.assertEqual(len(all_transforms), self.expected_nbr_transforms + nbr_extra_transforms_expected)

    def test_abc_factory(self):
        """Test the most basic form of the factory which ignores input_strings and output_strings"""
        ts = transforms.TransformLowercase.factory([], [])
        self.assertEqual(len(ts), 1)

    def test_RemoveWords_factory(self):
        # an empty list of input strings means no RemoveWords transformers
        ts = transforms.TransformRemoveWords.factory([], [])
        self.assertEqual(len(ts), 0)

        # if we provide 4 distinct input_string tokens, we expect 4
        # transformers
        input_strings = ["x y z", "a y"]
        output_strings = ["", ""]
        ts = transforms.TransformRemoveWords.factory(input_strings, output_strings)
        self.assertEqual(len(ts), 4)

        tokens_seen = []
        for t in ts:
            tokens_seen.append(t.terms)
        # check we only see 4 tokens with no repeats
        self.assertEqual(len(set(tokens_seen)), 4)


class TestCase1(unittest.TestCase):
    def test1(self):
        t = transforms.TransformRemoveDot00()
        result = t.apply(EMPTY_STRING)
        self.assertEqual(result, EMPTY_STRING)

        res = t.apply(ITEM1[0])
        self.assertEqual(res, ITEM1[1])

    def test2(self):
        t = transforms.TransformExpandK()
        res = t.apply(EMPTY_STRING)
        self.assertEqual(res, EMPTY_STRING)

        res = t.apply(ITEM2[0])
        self.assertEqual(res, ITEM2[1])

    def test3(self):
        t = transforms.TransformExtractNumber()
        res = t.apply(EMPTY_STRING)
        self.assertEqual(res, EMPTY_STRING)

        res = t.apply(ITEM3[0])
        self.assertEqual(res, ITEM3[1])

    def test4(self):
        t = transforms.TransformSpokenWordsToNumbers()

        res = t.apply(ITEM4[0])
        self.assertEqual(res, ITEM4[1])

        res = t.apply(ITEM5[0])
        self.assertEqual(res, ITEM5[1])

    #def test5(self):
        #t = transforms.TransformFTFY()
        #res = t.apply(ITEM6[0])
        #self.assertEqual(res, ITEM6[1])

        ## check for a no-op
        #res = t.apply(ITEM4[0])
        #self.assertEqual(res, ITEM4[0])

    def test6(self):
        t = transforms.TransformUnidecode()
        res = t.apply(ITEM7[0])
        self.assertEqual(res, ITEM7[1])

    def testRemoveWords(self):
        t = transforms.TransformRemoveWords()
        inp, expected_res, terms = WORDS_TO_REMOVE
        t.configure(terms=terms)
        self.assertEqual(t.terms, "ltd")
        res = t.apply(inp)
        self.assertEqual(res, expected_res)
