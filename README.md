
    $ python learning_text_transformer/learner3.py data/salaries_simple.csv 
    Loaded 7 items from data/salaries_simple.csv
    ====
    Final sequence of transforms: (<transforms.TransformExpandK object at 0x7f93d13d5eb8>, <transforms.TransformExtractNumber object at 0x7f93d13d5f60>)

    $ python learning_text_transformer/learner3.py data/companies_simple.csv


Installation:

    * $ python setup.py develop
    * $ nosetests
    * $ py.test -s -v

To trial it:

    $ python learning_text_transformer/server.py
    >>> import requests
    >>> import json
    >>> query={'from':['this Ltd', 'this blah'], 'to':['this', 'this blah']}
    >>> URL="http://api.annotate.io/learn"
    >>> URL="http://localhost:5000/learn"
    >>> requests.post(URL, data=json.dumps(query), headers={'Content-Type': 'application/json'}).json()

To add:

    * remove suffix words (needs to identify its own terms ahead of time)
    * show how to use pandas to upload a column
    * normalise units ml/l, cm/mm/m, inches
    * lowercase/uppercase all
    * replace variant dashes to - (partially done with unidecode)

    * force some Transform ordering e.g. FTFY first only
    * can we specify types in the final version? e.g. transform to an int?
    * may be want to represent tokenised items as nodes so e.g. order could be messed with?
    * prioritise Transforms so most likely to be useful are tried early
    * only build RemoveWords transformer if words aren't in destination string! else operation is redundant for that example


Possibly useful libraries:

    * http://txt2re.com/  make regexes semi-automatically
    * http://stackoverflow.com/questions/776286/given-a-string-generate-a-regex-that-can-parse-similar-strings
    * http://regex.inginf.units.it/ generate regexs automatically
    * https://pypi.python.org/pypi/num2words convert words to numbers (in various languages)
    * https://github.com/ghewgill/text2num/blob/master/text2num.py convert words to numbers
    * https://pypi.python.org/pypi/inflect  Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words.
    * http://code.activestate.com/recipes/52213/ soundex
    * http://pint.readthedocs.org/en/0.6/ unit conversion

Examples:

https://pawelmhm.github.io/python/pandas/2015/01/01/python-job-analytics.html analysing job data, notes that dates can be longform or 'just now' or 'yesterday' so good for mapping. 


PROBLEM
with new Clever search it doesn't explore all the options - why not?
python learning_text_transformer/learner3.py data/companies_simple.csv 
why not RemoveWords?
