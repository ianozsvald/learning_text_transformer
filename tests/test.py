"""Some tests"""
import unittest
from learning_text_transformer import transforms

EMPTY_STRING = ""
ITEM1 = ("30000.00", "30000")
ITEM2 = ("30K", "30000")
ITEM3 = ("blah 40 blah", "40")
ITEM4 = ("forty four", "44")
ITEM5 = ("thirty-three thousand", "33000")

# spoken word converter breaks on:
# "forty four hundred" -> "40400"


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
        #res = t.apply(EMPTY_STRING)
        #self.assertEqual(res, EMPTY_STRING)

        res = t.apply(ITEM4[0])
        self.assertEqual(res, ITEM4[1])

        res = t.apply(ITEM5[0])
        self.assertEqual(res, ITEM5[1])

