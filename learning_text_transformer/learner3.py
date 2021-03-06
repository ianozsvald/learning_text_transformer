##!/usr/bin/env python
"""Search for sequences of transforms that solve a task"""
import time
import copy
import abc
from collections import namedtuple
import csv
import argparse
import statistics
import Levenshtein
import ftfy
from learning_text_transformer import transforms
from learning_text_transformer import config


# DUMMY DECORATOR FOR PROFILING
def profile(target):
    def wrapper(*args, **kwargs):
        return target(*args, **kwargs)
    return wrapper


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
    #def get_best_transform_sequence(self, distances_and_sequences):
        #distances_and_sequences.sort(key=lambda x: x.average_distance)
        #chosen_transformations = distances_and_sequences[0].transformations
        #best_cost = distances_and_sequences[0].average_distance
        #return chosen_transformations, best_cost

    def apply_transforms(self, ts, s):
        """Apply list of Transform objects to string s, return transformed string"""
        change_made = False
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
    def __init__(self, conf=None, verbose=False, timeout=2):
        self.nbr_evals = 0
        self.best_distance = None
        self.best_cur_seq = None
        self.conf = conf
        self.verbose = verbose
        self.timeout = timeout  # seconds for max search time

    def calculate_distance(self, s1, s2):
        return Levenshtein.distance(s1, s2)

    @profile
    def evaluate_transforms(self, cur_seq, examples_to_learn_from, force_evaluation=False):
        self.nbr_evals += 1
        if self.verbose:
            if self.nbr_evals % 10000 == 0:
                print("...nbr_evals", self.nbr_evals, cur_seq)
        distances_per_example = []
        transform_made_a_change = False
        average_distance_for_this_sequence = None
        for example_nbr, (s1, s2) in enumerate(examples_to_learn_from):
            s1, change_made = self.apply_transforms(cur_seq, s1)
            if change_made:
                transform_made_a_change = True
            #distance = 1.0 - Levenshtein.ratio(s1, s2)
            #distance = Levenshtein.distance(s1, s2)
            distance = self.calculate_distance(s1, s2)
            distances_per_example.append(distance)

        if transform_made_a_change or force_evaluation:
            average_distance_for_this_sequence = statistics.mean(distances_per_example)
        return average_distance_for_this_sequence, transform_made_a_change

    @profile
    def search_transforms(self, ts, cur_seq, examples_to_learn_from):
        # ts - current set of operators we need to search
        # cur_seq - sequence of operators we're investigating
        assert self.best_distance is not None
        assert self.best_cur_seq is not None
        keep_going = True
        if time.time() > self.finish_search_by:
            # if we've exceeded our allowed search time we must exit
            keep_going = False
            if self.verbose:
                print("TIMED OUT!", examples_to_learn_from)
        # before we try new moves, get a score for the moves we had before
        average_distance_cur_seq, _ = self.evaluate_transforms(cur_seq, examples_to_learn_from, force_evaluation=True)
        for idx in range(len(ts)):
            t = ts.pop(idx)
            cur_seq.append(t)
            average_distance_for_this_sequence, transform_made_a_change = self.evaluate_transforms(cur_seq, examples_to_learn_from)
            new_move_improves_the_score = False
            if transform_made_a_change:
                new_move_improves_the_score = average_distance_for_this_sequence < average_distance_cur_seq
                if average_distance_for_this_sequence < self.best_distance:
                    self.best_distance = average_distance_for_this_sequence
                    self.best_cur_seq = copy.copy(cur_seq)
                    if self.verbose:
                        print("New best", self.best_distance, self.best_cur_seq, self.nbr_evals, average_distance_cur_seq)

                # if we've found a perfect solution then stop trying
                if average_distance_for_this_sequence == 0:
                    keep_going = False
            # recursively explore this tree if the latest Transform made a
            # change to at least 1 example
            if keep_going and transform_made_a_change and new_move_improves_the_score:
                keep_going = self.search_transforms(ts, cur_seq, examples_to_learn_from)
            cur_seq.pop()
            ts.insert(idx, t)
        return keep_going

    @profile
    def search_permutations(self, examples_to_learn_from, verbose):
        self.nbr_evals = 0
        # set a maximum timeout
        self.finish_search_by = time.time() + self.timeout

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
        self.best_distance, _ = self.evaluate_transforms(cur_seq, examples_to_learn_from, force_evaluation=True)
        self.best_cur_seq = []
        self.search_transforms(ts, cur_seq, examples_to_learn_from)
        return cur_seq, ts

    @profile
    def search_and_find_best_sequence(self, examples_to_learn_from, verbose=False):
        examples_to_learn_from = self.fix_unicode(examples_to_learn_from)
        input_strings, output_strings = [], []
        for frm, to in examples_to_learn_from:
            input_strings.append(frm)
            output_strings.append(to)

        t1 = time.time()
        permutations_tested, transforms_tested = self.search_permutations(examples_to_learn_from, verbose)

        chosen_transformations = self.best_cur_seq
        best_cost = self.best_distance
        if verbose:
            print("Took {0:.2f}s to find best sequence".format(time.time() - t1))

        return chosen_transformations, best_cost


def get_transform_searcher(conf=None, verbose=False, timeout=30):
    return TransformSearcherClever(conf, verbose=verbose, timeout=timeout)


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

    print("\nTransformed versions of the input sequences:")
    for frm, to in examples_to_learn_from[1:]:
        transformed_frm, _ = transform_searcher.apply_transforms(chosen_transformations, frm)
        print("'{}'->'{}' compared to '{}' has distance '{}'".format(frm, transformed_frm, to, transform_searcher.calculate_distance(transformed_frm, to)))

    #print(transform_searcher.evaluate_transforms(chosen_transformations, examples_to_learn_from, force_evaluation=True))
