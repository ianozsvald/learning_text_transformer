import re
from pprint import pprint
from collections import namedtuple
import csv
import argparse
import pandas as pd
import numpy as np
import Levenshtein
from itertools import permutations, chain
from transforms import TransformExtractNumber, TransformExpandK, TransformRemoveDot00

# how to deal with the (a-b) version?
#
# needs unittests for each transform!
# can we specify types in the final version? e.g. transform to an int?
# may be want to represent tokenised items as nodes so e.g. order could be
# messed with?


TRANSFORMS = [TransformExtractNumber(), TransformExpandK(), TransformRemoveDot00()]

# make it print wide!
pd.set_option('display.expand_frame_repr', False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('input_file', type=str, help='CSV file of mappings to learn')
    parser.add_argument('--verbose', default=False, action="store_true")
    args = parser.parse_args()

    verbose = args.verbose

    # load data that we'll learn from
    with open(args.input_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header==["From", "To"]
        examples_to_learn_from = [l for l in reader]
    print("Loaded {} items from {}".format(len(examples_to_learn_from), args.input_file))

    #ScoredTransform = namedtuple('ScoredTransform', ['operation', 'original', 'transformed', 'goal', 'distance'])
    ScoredTransformation = namedtuple('ScoredTransformation', ['transformations', 'average_distance'])
    #examples_to_learn_from = EXAMPLES
    #assert examples_to_learn_from == lines

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
        if verbose:
            print(transform_permutation)
        distances_per_example = []
        for example_nbr, example in enumerate(examples_to_learn_from):
            s1, s2 = example
            for transform_nbr, transform in enumerate(transform_permutation):
                s1_transformed = transform.apply(s1)
                s1 = s1_transformed
            distance = 1.0 - Levenshtein.ratio(s1, s2)
            distances_per_example.append(distance)
        average_distance_for_this_sequence = np.mean(distances_per_example)
        if verbose:
            print(distances_per_example, average_distance_for_this_sequence)
        distances_and_sequences.append(ScoredTransformation(transform_permutation, average_distance_for_this_sequence))

    distances_and_sequences.sort(key=lambda x: x.average_distance)
    if verbose:
        print()
        pprint(distances_and_sequences)

    chosen_transformations = distances_and_sequences[0].transformations

    print("====")
    print("Final sequence of transforms:", chosen_transformations)
