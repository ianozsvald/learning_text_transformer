import re
from pprint import pprint
from collections import namedtuple
import pandas as pd
import numpy as np
import Levenshtein
import examples
from itertools import permutations, chain

# how to deal with the (a-b) version?
#
# needs unittests for each transform!
# can we specify types in the final version? e.g. transform to an int?
# may be want to represent tokenised items as nodes so e.g. order could be
# messed with?


#def transform_noop(s):
    #"""do nothing operation"""
    #return s


def transform_extract_number(s):
    """return first contiguous number or no change"""
    result = re.findall("\D*(\d+).*", s)
    if result:
        return result[0]
    return s  # don't transform as a default


def transform_expand_k(s):
    return s.replace('K', '000')


def transform_remove_dot00(s):
    return s.replace('.00', '')

# these 2 don't work with naive 1 depth search
EXAMPLES = [examples.EX_SP_1, examples.EX_SP_2, examples.EX_SP_3, examples.EX_SP_4, examples.EX_SP_5, examples.EX_SP_6, examples.EX_SP_7]

TRANSFORMS = [transform_extract_number, transform_expand_k, transform_remove_dot00]

# make it print wide!
pd.set_option('display.expand_frame_repr', False)

if __name__ == "__main__":
    #ScoredTransform = namedtuple('ScoredTransform', ['operation', 'original', 'transformed', 'goal', 'distance'])
    ScoredTransformation = namedtuple('ScoredTransformation', ['transformations', 'average_distance'])
    examples_to_learn_from = EXAMPLES

    # make 1 to full-length list of all permutations
    #perms = list(permutations(TRANSFORMS, len(TRANSFORMS)))  # just do full-length permutations
    perms=[]
    l2 = list(chain(permutations(TRANSFORMS, rng)) for rng in range(1, len(TRANSFORMS)+1))
    for item in l2:
      perms += item

    # for each permutation of the possible transformations
    operation_distances = np.zeros((len(examples_to_learn_from), len(TRANSFORMS)))
    distances_and_sequences = []
    for transform_permutation in perms:
        print(transform_permutation)
        distances_per_example = []
        for example_nbr, example in enumerate(examples_to_learn_from):
            s1, s2 = example
            for transform_nbr, transform in enumerate(transform_permutation):
                s1_transformed = transform(s1)
                s1 = s1_transformed
            distance = 1.0 - Levenshtein.ratio(s1, s2)
            distances_per_example.append(distance)
        average_distance_for_this_sequence = np.mean(distances_per_example)
        print(distances_per_example, average_distance_for_this_sequence)
        distances_and_sequences.append(ScoredTransformation(transform_permutation, average_distance_for_this_sequence))

    print()
    distances_and_sequences.sort(key=lambda x: x.average_distance)
    pprint(distances_and_sequences)

    chosen_transformations = distances_and_sequences[0].transformations

    print("====")
    print("Final sequence of transforms:", chosen_transformations)
