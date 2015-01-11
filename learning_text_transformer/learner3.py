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


# TODO
# do ftfy on incoming text, not during search


def load_examples(input_file):
    """Load data that we'll learn from"""
    with open(input_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["From", "To"]
        examples_to_learn_from = [l for l in reader]
    return examples_to_learn_from

ScoredTransformation = namedtuple('ScoredTransformation', ['transformations', 'average_distance'])

class TransformSearcherBase(abc.ABC):
    def get_best_transform_sequence(self, distances_and_sequences):
        distances_and_sequences.sort(key=lambda x: x.average_distance)
        chosen_transformations = distances_and_sequences[0].transformations
        best_cost = distances_and_sequences[0].average_distance
        return chosen_transformations, best_cost

    def apply_transforms(self, ts, s):
        """Apply list of Transform objects to string s, return transformed string"""
        s = ftfy.fix_text(s)  # fix any bad unicode
        transform_always_made_changes = True
        for transform_nbr, t in enumerate(ts):
            s1 = t.apply(s)
            if s1 == s:
                transform_always_made_changes = False
            s = s1
        return s, transform_always_made_changes

import copy
class TransformSearcherClever(TransformSearcherBase):
    def __init__(self):
        self.nbr_evals = 0
        self.best_distance = None
        self.best_cur_seq = None

    def evaluate_transforms(self, cur_seq, examples_to_learn_from):
        self.nbr_evals += 1
        if self.nbr_evals % 1000 == 0:
            print("nbr_evals", self.nbr_evals, cur_seq)
        #verbose = False
        #if verbose:
            #print(transform_permutation)
        distances_per_example = []
        transform_made_a_change = True
        for example_nbr, (s1, s2) in enumerate(examples_to_learn_from):
            s1, transform_always_made_changes = self.apply_transforms(cur_seq, s1)
            if not transform_always_made_changes:
                transform_made_a_change = False
            distance = 1.0 - Levenshtein.ratio(s1, s2)
            distances_per_example.append(distance)

        average_distance_for_this_sequence = statistics.mean(distances_per_example)
        #print("evaluation:", cur_seq, average_distance_for_this_sequence, nbr_evals)
        return average_distance_for_this_sequence, transform_made_a_change

    def search_transforms(self, ts, cur_seq, examples_to_learn_from):
        #print("Searching using:", cur_seq)
        #best_distance, best_cur_seq
        keep_going = True
        for idx in range(len(ts)):
            if not keep_going:
                continue
            t = ts.pop(idx)
            cur_seq.append(t)
            average_distance_for_this_sequence, transform_made_a_change = self.evaluate_transforms(cur_seq, examples_to_learn_from)
            if self.best_distance is None or average_distance_for_this_sequence < self.best_distance:
                self.best_distance = average_distance_for_this_sequence
                self.best_cur_seq = copy.copy(cur_seq)
                print("New best", self.best_distance, self.best_cur_seq, self.nbr_evals)

            if average_distance_for_this_sequence == 0:
                keep_going = False
            if keep_going and transform_made_a_change:
                keep_going = self.search_transforms(ts, cur_seq, examples_to_learn_from)
            #if not transform_made_a_change:
                #print("Skipping...")
            cur_seq.pop()
            ts.insert(idx, t)
        return keep_going

    def search_permutations(self, examples_to_learn_from, verbose):
        self.nbr_evals = 0
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        ts = transforms.get_transforms(input_strings, output_strings)
        print("SEARCHING USING:")
        for t in ts:
            print(t)
        cur_seq = []
        self.search_transforms(ts, cur_seq, examples_to_learn_from)
        return cur_seq, ts

    def search_and_find_best_sequence(self, examples_to_learn_from, verbose=False):
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        t1 = time.time()
        permutations_tested, transforms_tested = self.search_permutations(examples_to_learn_from, verbose)
        if verbose:
            print("Tested {} of {} permutations using {} transforms".format(permutations_tested, len(perms), transforms_tested))

        t1 = time.time()
        #chosen_transformations, best_cost = self.get_best_transform_sequence(distances_and_sequences)
        chosen_transformations = self.best_cur_seq
        best_cost = self.best_distance
        if verbose:
            print("Took {0:.2f}s to find best sequence".format(time.time() - t1))

        if verbose:
            print()
            pprint(distances_and_sequences)

        return chosen_transformations, best_cost




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
                s1, transform_always_made_changes = self.apply_transforms(transform_permutation, s1)
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


def get_transform_searcher():
    #return TransformSearcherClever()
    return TransformSearcherPermutations()


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
