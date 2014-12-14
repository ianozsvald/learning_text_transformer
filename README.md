
    $ python learning_text_transformer/learner3.py data/salaries_simple.csv 
    Loaded 7 items from data/salaries_simple.csv
    ====
    Final sequence of transforms: (<transforms.TransformExpandK object at 0x7f93d13d5eb8>, <transforms.TransformExtractNumber object at 0x7f93d13d5f60>)

    $ python learning_text_transformer/learner3.py data/companies_simple.csv

To add:

    * normalise repeated spaces and trim whitespace
    * normalise units ml/l, cm/mm/m, inches
    * convert unicode to ascii
    * fix bad unicode
    * lowercase/uppercase all
    * remove suffix words

    * can we specify types in the final version? e.g. transform to an int?
    * may be want to represent tokenised items as nodes so e.g. order could be messed with?

Possibly useful libraries:

    * http://txt2re.com/  make regexes semi-automatically
    * http://stackoverflow.com/questions/776286/given-a-string-generate-a-regex-that-can-parse-similar-strings
    * http://regex.inginf.units.it/ generate regexs automatically
    * https://pypi.python.org/pypi/num2words convert words to numbers (in various languages)
    * https://github.com/ghewgill/text2num/blob/master/text2num.py convert words to numbers
    * https://pypi.python.org/pypi/inflect  Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words.
