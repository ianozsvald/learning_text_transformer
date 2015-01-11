from pprint import pprint
import time
import abc
from collections import namedtuple
import csv
import argparse
import statistics
import Levenshtein
import ftfy
from itertools import permutations, chain
from learning_text_transformer import transforms


def load_examples(input_file):
    """Load data that we'll learn from"""
    with open(input_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["From", "To"]
        examples_to_learn_from = [l for l in reader]
    return examples_to_learn_from

ScoredTransformation = namedtuple('ScoredTransformation', ['transformations', 'average_distance'])

class TransformSearcherClever(object):
    def search_permutations(self, examples_to_learn_from, verbose):
        global nbr_evals
        nbr_evals = 0
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        ts = transforms.get_transforms(input_strings, output_strings)
        cur_seq = []
        search_transforms(ts, cur_seq, examples_to_learn_from)

    def search_and_find_best_sequence(self, examples_to_learn_from, verbose=False):
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        t1 = time.time()
        permutations_tested, transforms_tested, distances_and_sequences = search_permutations(self, examples_to_learn_from, verbose)
        if verbose:
            print("Tested {} of {} permutations using {} transforms".format(permutations_tested, len(perms), transforms_tested))

        t1 = time.time()
        chosen_transformations, best_cost = get_best_transform_sequence(distances_and_sequences)
        if verbose:
            print("Took {0:.2f}s to find best sequence".format(time.time() - t1))

        if verbose:
            print()
            pprint(distances_and_sequences)

        return chosen_transformations, best_cost


class TransformSearcherBase(abc.ABC):
    def get_best_transform_sequence(self, distances_and_sequences):
        distances_and_sequences.sort(key=lambda x: x.average_distance)
        chosen_transformations = distances_and_sequences[0].transformations
        best_cost = distances_and_sequences[0].average_distance
        return chosen_transformations, best_cost

def get_transform_searcher():
    return TransformSearcherPermutations()

class TransformSearcherPermutations(TransformSearcherBase):
    def make_permutations(self, examples_to_learn_from):
        """Make 1 to full-length list of all permutations"""
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)
        list_of_transforms = transforms.get_transforms(input_strings, output_strings)
        perms = []
        l2 = list(chain(permutations(list_of_transforms, rng)) for rng in range(1, len(list_of_transforms)+1))
        for item in l2:
            perms += item
        return perms

    def apply_transforms(self, ts, s):
        """Apply list of Transform objects to string s, return transformed string"""
        s = ftfy.fix_text(s)  # fix any bad unicode
        for transform_nbr, t in enumerate(ts):
            s = t.apply(s)
        return s


    def search_permutations(self, perms, examples_to_learn_from, verbose):
        """Test all permutations of Transforms, exit if a 0 distance solution is found"""
        distances_and_sequences = []
        permutations_tested = 0
        transforms_tested = 0
        for transform_permutation in perms:
            if verbose:
                print(transform_permutation)
            distances_per_example = []
            for example_nbr, (s1, s2) in enumerate(examples_to_learn_from):
                s1 = self.apply_transforms(transform_permutation, s1)
                transforms_tested += len(transform_permutation)
                distance = 1.0 - Levenshtein.ratio(s1, s2)
                distances_per_example.append(distance)

            average_distance_for_this_sequence = statistics.mean(distances_per_example)
            if verbose:
                print(distances_per_example, average_distance_for_this_sequence)
            distances_and_sequences.append(ScoredTransformation(transform_permutation, average_distance_for_this_sequence))
            permutations_tested += 1
            if average_distance_for_this_sequence == 0:
                break
        return permutations_tested, transforms_tested, distances_and_sequences

    def search_and_find_best_sequence(self, examples_to_learn_from, verbose=False):
        t1 = time.time()
        perms = self.make_permutations(examples_to_learn_from)
        if verbose:
            print("Took {0:.2f}s to make all permutations".format(time.time() - t1))
            print("Using {} permutations".format(len(perms)))

        permutations_tested, transforms_tested, distances_and_sequences = self.search_permutations(perms, examples_to_learn_from, verbose)
        if verbose:
            print("Tested {} of {} permutations using {} transforms".format(permutations_tested, len(perms), transforms_tested))

        t1 = time.time()
        chosen_transformations, best_cost = self.get_best_transform_sequence(distances_and_sequences)
        if verbose:
            print("Took {0:.2f}s to find best sequence".format(time.time() - t1))

        if verbose:
            print()
            pprint(distances_and_sequences)

        return chosen_transformations, best_cost


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('input_file', type=str, help='CSV file of mappings to learn')
    parser.add_argument('--verbose', default=False, action="store_true")
    args = parser.parse_args()

    verbose = args.verbose
    examples_to_learn_from = load_examples(args.input_file)
    print("Loaded {} items from {}".format(len(examples_to_learn_from), args.input_file))

    transform_searcher = get_transform_searcher()
    chosen_transformations, best_cost = transform_searcher.search_and_find_best_sequence(examples_to_learn_from, verbose)

    print("====")
    print("Final sequence of transforms (cost={}):".format(best_cost))
    for chosen_transformation in chosen_transformations:
        print(chosen_transformation)
