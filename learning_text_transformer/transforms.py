import abc
import re
from learning_text_transformer import spoken_word_to_number


# expandk should work on lowercase k e.g. 30k too?
# TransformExtractNumber should extract multiple numbers!
# TransformRemoveWords needs to be hardcoded with a list of terms

class Transform(abc.ABC):
    @abc.abstractmethod
    def apply(self, s):
        pass


class TransformExtractNumber(Transform):
    def apply(self, s):
        result = re.findall("\D*(\d+).*", s)
        if result:
            return result[0]
        return s  # don't transform as a default


class TransformExpandK(Transform):
    def apply(self, s):
        return s.replace('K', '000')


class TransformRemoveDot00(Transform):
    def apply(self, s):
        return s.replace('.00', '')


class TransformSpokenWordsToNumbers(Transform):
    def apply(self, s):
        try:
            s = str(spoken_word_to_number.spoken_word_to_number(s))
        except (KeyError, AssertionError):
            pass  # lots of things cause this converter to break
        return s


class TransformLowercase(Transform):
    def apply(self, s):
        return s.lower()


class TransformStrip(Transform):
    def apply(self, s):
        # strip multiple spaces
        s1 = re.sub("[\s]+", " ", s)
        return s1.strip()


class TransformRemoveWords(Transform):
    def __init__(self, terms):
        self.terms = terms
        #self.terms = ["Ltd", "ltd", "Limited", "limited"]

    def apply(self, s):
        for term in self.terms:
            s = s.replace(term, "")
        return s