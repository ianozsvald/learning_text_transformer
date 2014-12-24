import abc
import re
import ftfy
import unidecode
from learning_text_transformer import spoken_word_to_number


# expandk should work on lowercase k e.g. 30k too?
# TransformExtractNumber should extract multiple numbers!
# TransformRemoveWords needs to be hardcoded with a list of terms, should learn
# terms from input text
# spoken words to numbers must allow empty strings
# get_transforms needs cleanup


class Transform(abc.ABC):
    @abc.abstractmethod
    def apply(self, s):
        pass

    def configure(self, **kwargs):
        pass

    def __str__(self):
        return self.__class__.__name__

    def serialise(self):
        return self.__class__.__name__, dict()

    @classmethod
    def deserialise(cls, parameters):
        c = cls()
        return c


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
    def configure(self, **kwargs):
        self.terms = kwargs['terms']
        #input_strings = kwargs['input_strings']
        #self.tokens = set()
        #for input_string in input_strings:
            #self.tokens.update([tok.strip() for tok in input_string.split()])

    @classmethod
    def deserialise(cls, parameters):
        c = cls()
        c.terms = parameters['terms']
        return c

    def serialise(self):
        return self.__class__.__name__, {"terms": self.terms}

    def apply(self, s):
        for term in self.terms:
            s = s.replace(term, "")
        return s

    def __str__(self):
        return self.__class__.__name__ + "(" + repr(self.terms) + ")"


class TransformFTFY(Transform):
    def apply(self, s):
        return ftfy.fix_text(s)


class TransformUnidecode(Transform):
    def apply(self, s):
        return unidecode.unidecode(s)


def deserialise_transform(transform_name, parameters):
    """"""
    for transform_cls in Transform.__subclasses__():
        if transform_cls.__name__ == transform_name:
            return transform_cls.deserialise(parameters)
    else:
        raise ValueError()


def get_transforms():
    all_transforms = []
    for transform in Transform.__subclasses__():
        t = [transform()]
        if t[0].__class__.__name__ == "TransformRemoveWords":
            t = []
            for term in ["Ltd", "Limited"]:
                t_new = transform()
                t_new.configure(terms=[term])
                t.append(t_new)

        all_transforms += t

    return all_transforms


#def get_transformsX(mod):
    #transforms = []
    #for c in dir(mod):
        #print(c)
        #c = getattr(mod, c)
        #try:
            #if c is Transform:
                #continue
            #if issubclass(c, Transform):
                #transforms.append(c)
        #except TypeError:
            #pass
    #return transforms
