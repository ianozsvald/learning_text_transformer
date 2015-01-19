
    $ python learning_text_transformer/learner3.py data/salaries_simple.csv 
    Loaded 7 items from data/salaries_simple.csv
    ====
    Final sequence of transforms: (<transforms.TransformExpandK object at 0x7f93d13d5eb8>, <transforms.TransformExtractNumber object at 0x7f93d13d5f60>)

    $ python learning_text_transformer/learner3.py data/companies_simple.csv


Deployment:

    * cd /home/ianozsvald/webapps/api_annotate_io/learning_text_transformer
    * git pull
    * git checkout deploy
    * ../apache2/bin/stop
    * ../apache2/bin/start
    * curl api.annotate.io  # confirm we get a JSON response
    * /home/ianozsvald/logs/user/access_api_annotate_io.log  # access log
    * /home/ianozsvald/logs/user/error_api_annotate_io.log  # error log

Installation:

    * $ python setup.py develop
    * $ nosetests
    * $ py.test -s -v
    * py.test --cov learning_text_transformer --cov-report html

To trial it:

    $ python learning_text_transformer/server.py
    >>> import requests
    >>> import json
    >>> query={'from':['this Ltd', 'this blah'], 'to':['this', 'this blah']}
    >>> URL="http://api.annotate.io/learn"
    >>> URL="http://localhost:5000/learn"
    >>> requests.post(URL, data=json.dumps(query), headers={'Content-Type': 'application/json'}).json()

To add:

    * lowercase/uppercase all
    * replace variant dashes to - (partially done with unidecode)

    * show how to use pandas to upload a column
    * normalise units ml/l, cm/mm/m, inches
    * prioritise Transforms so most likely to be useful are tried early, e.g. use evidence of nbr of times it makes a change to prioritise it?
    * only build RemoveWords transformer if words aren't in destination string! else operation is redundant for that example

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

Calvin's request
"No examples to hand at present but the problem is really in detecting .tld and .tl.dd style domains. There is in theory a defined set but they change a lot. Then add in .wordpress.com, .blogspot.com etc which all have a set of unique sites under them. From the other end, loose www. api. etc but keep drive.google, groceries.tesco etc.

In essence, we want to group by the highest domain part that contains a single brand. We then want a tree of their interesting sub domains. "
