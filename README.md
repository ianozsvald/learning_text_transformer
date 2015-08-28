

# Status

First open release (Aug 2015), the docs need improving

# License

MIT (see license file)

# Goal

This learns to transform "the data that I have" into "the data that I want", you provide pairs of data (the "input" and the desired "output") and it tries to figure out a sequence of text transformations that'll solve this challenge.

The algorithm searches a large of possible transformations, it isn't guaranteed to find a solution as the search space can be crazy-big. This needs improving...

The current demo prints the sequence to screen but doesn't let you use it. The online version (http://annotate.io) has a demo that takes the generated transformation sequence and lets you use it to process your own data. The local demo will be updated just as soon as someone nags me.

*What I'd like* is for folk to tell me what they need - your use cases (with data!) and how this could save you time, that'll give me good reason to plug on with better implementations.


# Demo:

```
    # salaries_simple.csv
    From,To
    "£34866 P.A.","34866"
    "£48260 P.A.","48260"
    "60000.00","60000"
    "60K","60000"
    "45000","45000"
    "£60K","60000"
    "45000 + BONUS","45000"
    "thirty three thousand","33000"
    

    $ python learning_text_transformer/learner3.py data/salaries_simple.csv 
    Loaded 8 items from data/salaries_simple.csv
    ====
    Final sequence of transforms (cost=0.0):
    TransformExpandK()
    TransformRemoveDot00()
    TransformRemoveWords('+')
    TransformRemoveWords('P.A.')
    TransformRemoveWords('BONUS')
    TransformSpokenWordsToNumbers()
    TransformExtractNumber()

    Transformed versions of the input sequences:
    '£48260 P.A.'->'48260' compared to '48260' has distance '0'
    '60000.00'->'60000' compared to '60000' has distance '0'
    '60K'->'60000' compared to '60000' has distance '0'
    '45000'->'45000' compared to '45000' has distance '0'
    '£60K'->'60000' compared to '60000' has distance '0'
    '45000 + BONUS'->'45000' compared to '45000' has distance '0'
    'thirty three thousand'->'33000' compared to '33000' has distance '0'
```




# Demo as a server:

The core code is hosted using Flask at http://annotate.io, this lets you upload a JSON dictionary of "input" and "output" items, it'll then return an object representing the transformation sequence. You can upload this with new "input" data and it'll transform it for you.

```
    $ python learning_text_transformer/server.py
    >>> import requests
    >>> import json
    >>> query={'inputs':['this Ltd', 'this blah'], 'outputs':['this', 'this blah']}
    >>> # URL="http://api.annotate.io/learn" # use this for the online demo
    >>> URL="http://localhost:5000/learn"
    >>> requests.post(URL, data=json.dumps(query), headers={'Content-Type': 'application/json'}).json()
    {'transforms': [['TransformRemoveWords', {'terms': 'Ltd'}],
                    ['TransformStrip', {}]]}
```  

# Further demo (via online version):

```
    $ python demo/annotateio_demo.py  # run the demo, it talks to annotate.io

    Annotate.io demo  to show how we learn a transformation sequence for data cleaning

    Training phase - we use `inputs` to learn a transformation to get to the desired `outputs`:
    inputs: ['Accenture PLC', 'Accenture Europe', 'Société Générale', 'SociÃ©tÃ© GÃ©nÃ©rale']
    outputs: ['accenture', 'accenture europe', 'societe generale', 'societe generale']
    Calling Annotate.io...
    Training phase complete, now we have a `transforms` code

    Data cleaning phase - we use the `transforms` that we've learned on previously unseen `inputs` items to generate new `outputs`):
    inputs: ['RBS PLC', 'Royal Bank of Scotland PLC', 'Lancôme', ' Estée Lauder  ']
    We now have a transformed result:
    outputs: ['rbs', 'royal bank of scotland', 'lancome', 'estee lauder']

    Pretty printed:
        Previously unseen input:                Annotate's output:
                           RBS PLC ->                            rbs
        Royal Bank of Scotland PLC ->         royal bank of scotland
                           Lancôme ->                        lancome
                    Estée Lauder   ->                   estee lauder

    The transforms that are used in this demo include: Lowercase, Strip white-space, Convert unicode to ASCII, Strip token (to remove 'Ltd'), Fix badly encoded unicode

```

# Installation:

    * $ python setup.py develop
    * $ py.test
    
    # For debugging
    * $ py.test -s -v # shows stdout and verbose info 

    # Adding coverage and generating a report in ./html
    * $ py.test --cov learning_text_transformer --cov-report html



# To add:

    * lowercase/uppercase all
    * replace variant dashes to - (partially done with unidecode)
    * make it faster! switch to e.g. A* algorithm

# Possibilities...
    * show how to use pandas to upload a column
    * normalise units ml/l, cm/mm/m, inches
    * prioritise Transforms so most likely to be useful are tried early, e.g. use evidence of nbr of times it makes a change to prioritise it?
    * only build RemoveWords transformer if words aren't in destination string! else operation is redundant for that example

Problems:

    * ATTRACTIVE SALARY PACKAGE -> "000" due to expandk not checking for nbr!
    * mean was expensive, something that needs checking
    * levenshtein.ratio didn't do a score for very distance strings, so no error space! i switched to raw edit distance

Future ideas?
 
    * can we specify types in the final version? e.g. transform to an int?
    * if we specify the output type (e.g. int) we can use L2 norm as a distance metric on numeric outputs (maybe, but then how to score the text transforms inbetween?)
    * may be want to represent tokenised items as nodes so e.g. order could be messed with?


Possibly useful libraries:

    * http://txt2re.com/  make regexes semi-automatically
    * http://stackoverflow.com/questions/776286/given-a-string-generate-a-regex-that-can-parse-similar-strings
    * http://regex.inginf.units.it/ generate regexs automatically
    * https://pypi.python.org/pypi/num2words convert words to numbers (in various languages)
    * https://pypi.python.org/pypi/inflect  Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words.
    * http://code.activestate.com/recipes/52213/ soundex
    * http://pint.readthedocs.org/en/0.6/ unit conversion
    * https://github.com/sunlightlabs/jellyfish  approximate/phonetic string matching inc Lev, Soundex, Metaphone

Examples:

https://pawelmhm.github.io/python/pandas/2015/01/01/python-job-analytics.html analysing job data, notes that dates can be longform or 'just now' or 'yesterday' so good for mapping. 

