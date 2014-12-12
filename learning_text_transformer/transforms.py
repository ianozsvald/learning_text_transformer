import abc
import re
from learning_text_transformer import spoken_word_to_number


# expandk should work on lowercase k e.g. 30k too?
#

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
