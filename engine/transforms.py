import abc
import re


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
