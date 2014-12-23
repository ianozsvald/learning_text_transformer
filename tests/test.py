"""Some tests"""
import unittest
from learning_text_transformer import transforms

EMPTY_STRING = ""
# most items are (inp, expected_result) and t.apply(inp)->res
ITEM1 = ("30000.00", "30000")
ITEM2 = ("30K", "30000")
ITEM3 = ("blah 40 blah", "40")
ITEM4 = ("forty four", "44")
ITEM5 = ("thirty-three thousand", "33000")
ITEM6 = ("schÃ¶n", "schön")
ITEM7 = ("société", "societe")

WORDS_TO_REMOVE = ("this thing ltd", "this thing ", ["ltd"])
# spoken word converter breaks on:
# "forty four hundred" -> "40400"
# empty input string


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

    def test5(self):
        t = transforms.TransformFTFY()
        res = t.apply(ITEM6[0])
        self.assertEqual(res, ITEM6[1])

        # check for a no-op
        res = t.apply(ITEM4[0])
        self.assertEqual(res, ITEM4[0])

    def test6(self):
        t = transforms.TransformUnidecode()
        res = t.apply(ITEM7[0])
        self.assertEqual(res, ITEM7[1])

    def testRemoveWords(self):
        t = transforms.TransformRemoveWords()
        inp, expected_res, terms = WORDS_TO_REMOVE
        t.configure(terms=terms)
        res = t.apply(inp)
        self.assertEqual(res, expected_res)

        self.assertEqual(t.terms, ["ltd"])
