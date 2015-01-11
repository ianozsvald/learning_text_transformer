from pprint import pprint
import time
import copy
import abc
from collections import namedtuple
import csv
import argparse
import statistics
import Levenshtein
import ftfy
from itertools import permutations, chain
from learning_text_transformer import transforms
from learning_text_transformer import config


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
        for transform_nbr, t in enumerate(ts):
            s1 = t.apply(s)
            change_made = False
            if s1 != s:
                change_made = True
            s = s1
        # signal if a change was made on the last transform
        return s, change_made

    def fix_unicode(self, examples_to_learn_from):
        fixed_examples_to_learn_from = []
        for frm, to in examples_to_learn_from:
            frm = ftfy.fix_text(frm)  # fix any bad unicode
            fixed_examples_to_learn_from.append((frm, to))
        return fixed_examples_to_learn_from


class TransformSearcherClever(TransformSearcherBase):
    def __init__(self, conf=None, verbose=False):
        self.nbr_evals = 0
        self.best_distance = None
        self.best_cur_seq = None
        self.conf = conf
        self.verbose = verbose

    def evaluate_transforms(self, cur_seq, examples_to_learn_from):
        self.nbr_evals += 1
        if self.verbose:
            if self.nbr_evals % 1000 == 0:
                print("nbr_evals", self.nbr_evals, cur_seq)
        #verbose = False
        #if verbose:
            #print(transform_permutation)
        distances_per_example = []
        transform_made_a_change = False
        for example_nbr, (s1, s2) in enumerate(examples_to_learn_from):
            s1, change_made = self.apply_transforms(cur_seq, s1)
            if change_made:
                transform_made_a_change = True
            distance = 1.0 - Levenshtein.ratio(s1, s2)
            distances_per_example.append(distance)

        average_distance_for_this_sequence = statistics.mean(distances_per_example)
        #print("evaluation:", cur_seq, average_distance_for_this_sequence, nbr_evals)
        return average_distance_for_this_sequence, transform_made_a_change

    def search_transforms(self, ts, cur_seq, examples_to_learn_from):
        # ts - current set of operators we need to search
        # cur_seq - sequence of operators we're investigating
        keep_going = True
        for idx in range(len(ts)):
            t = ts.pop(idx)
            cur_seq.append(t)
            average_distance_for_this_sequence, transform_made_a_change = self.evaluate_transforms(cur_seq, examples_to_learn_from)
            if transform_made_a_change:
                if self.best_distance is None or average_distance_for_this_sequence < self.best_distance:
                    self.best_distance = average_distance_for_this_sequence
                    self.best_cur_seq = copy.copy(cur_seq)
                    if self.verbose:
                        print("New best", self.best_distance, self.best_cur_seq, self.nbr_evals)

            # if we've found a perfect solution then stop trying
            if average_distance_for_this_sequence == 0:
                keep_going = False
            # recursively explore this tree if the latest Transform made a
            # change to at least 1 example
            if keep_going and transform_made_a_change:
                keep_going = self.search_transforms(ts, cur_seq, examples_to_learn_from)
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
        if verbose:
            print("SEARCHING USING:")
            for t in ts:
                print(t)
        cur_seq = []
        self.search_transforms(ts, cur_seq, examples_to_learn_from)
        return cur_seq, ts

    def search_and_find_best_sequence(self, examples_to_learn_from, verbose=False):
        examples_to_learn_from = self.fix_unicode(examples_to_learn_from)
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        t1 = time.time()
        permutations_tested, transforms_tested = self.search_permutations(examples_to_learn_from, verbose)
        #if verbose:
            #print("Tested {} of {} permutations using {} transforms".format(permutations_tested, len(perms), transforms_tested))

        #t1 = time.time()
        #chosen_transformations, best_cost = self.get_best_transform_sequence(distances_and_sequences)
        chosen_transformations = self.best_cur_seq
        best_cost = self.best_distance
        if verbose:
            print("Took {0:.2f}s to find best sequence".format(time.time() - t1))

        #if verbose:
            #print()
            #pprint(distances_and_sequences)

        return chosen_transformations, best_cost


def get_transform_searcher(conf=None):
    return TransformSearcherClever(conf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('input_file', type=str, help='CSV file of mappings to learn')
    parser.add_argument('--verbose', default=False, action="store_true")
    args = parser.parse_args()

    conf = config.get('dev')

    verbose = args.verbose
    examples_to_learn_from = load_examples(args.input_file)
    print("Loaded {} items from {}".format(len(examples_to_learn_from), args.input_file))

    transform_searcher = get_transform_searcher(conf, verbose)
    chosen_transformations, best_cost = transform_searcher.search_and_find_best_sequence(examples_to_learn_from, verbose)

    print("====")
    print("Final sequence of transforms (cost={}):".format(best_cost))
    for chosen_transformation in chosen_transformations:
        print(chosen_transformation)
