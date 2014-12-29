from pprint import pprint
from collections import namedtuple
import csv
import argparse
import numpy as np
import Levenshtein
from itertools import permutations, chain
import transforms


def make_permutations(input_strings, output_strings):
    """Make 1 to full-length list of all permutations"""
    list_of_transforms = transforms.get_transforms(input_strings, output_strings)
    perms = []
    l2 = list(chain(permutations(list_of_transforms, rng)) for rng in range(1, len(list_of_transforms)+1))
    for item in l2:
        perms += item
    return perms


def load_examples(input_file):
    """Load data that we'll learn from"""
    with open(input_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["From", "To"]
        examples_to_learn_from = [l for l in reader]
    return examples_to_learn_from


def search_permutations(perms, examples_to_learn_from):
    """Test all permutations of Transforms, exit if a 0 distance solution is found"""
    distances_and_sequences = []
    permutations_tested = 0
    transforms_tested = 0
    transforms_skipped = 0
    for transform_permutation in perms:
        if verbose:
            print(transform_permutation)
        distances_per_example = []
        for example_nbr, example in enumerate(examples_to_learn_from):
            s1, s2 = example
            for transform_nbr, transform in enumerate(transform_permutation):
                transforms_tested += 1
                s1_transformed = transform.apply(s1)
                s1 = s1_transformed
            distance = 1.0 - Levenshtein.ratio(s1, s2)
            distances_per_example.append(distance)
        average_distance_for_this_sequence = np.mean(distances_per_example)
        if verbose:
            print(distances_per_example, average_distance_for_this_sequence)
        distances_and_sequences.append(ScoredTransformation(transform_permutation, average_distance_for_this_sequence))
        permutations_tested += 1
        if average_distance_for_this_sequence == 0:
            break
    return permutations_tested, transforms_tested, distances_and_sequences


def get_best_transform_sequence(distances_and_sequences):
    distances_and_sequences.sort(key=lambda x: x.average_distance)
    chosen_transformations = distances_and_sequences[0].transformations
    best_score = distances_and_sequences[0].average_distance
    return chosen_transformations, best_score

ScoredTransformation = namedtuple('ScoredTransformation', ['transformations', 'average_distance'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('input_file', type=str, help='CSV file of mappings to learn')
    parser.add_argument('--verbose', default=False, action="store_true")
    args = parser.parse_args()

    verbose = args.verbose
    examples_to_learn_from = load_examples(args.input_file)
    print("Loaded {} items from {}".format(len(examples_to_learn_from), args.input_file))

    input_strings, output_strings = [], []
    for frm, to in examples_to_learn_from:
        input_strings.append(frm)
        output_strings.append(to)

    perms = make_permutations(input_strings, output_strings)
    print("Using {} permutations".format(len(perms)))

    permutations_tested, transforms_tested, distances_and_sequences = search_permutations(perms, examples_to_learn_from)
    print("Tested {} of {} permutations using {} transforms".format(permutations_tested, len(perms), transforms_tested))

    chosen_transformations, best_score = get_best_transform_sequence(distances_and_sequences)

    if verbose:
        print()
        pprint(distances_and_sequences)

    print("====")
    print("Final sequence of transforms (cost={}):".format(best_score))
    for chosen_transformation in chosen_transformations:
        print(chosen_transformation)
