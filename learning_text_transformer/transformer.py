##!/usr/bin/env python
"""Interface to setup a learning task and use the resulting transforms"""
import argparse
import learner3 as learner


class Transformer(object):
    def __init__(self, verbose=False):
        conf = None
        self.verbose = verbose
        self.transform_searcher = learner.get_transform_searcher(conf, self.verbose)

    def fit(self, examples_to_learn_from):
        """Fit pairs of inputs to outputs, this is a list of pairs"""
        self.check_format_of_examples_to_learn_from(examples_to_learn_from)
        self.chosen_transformations_, self.best_cost_ = self.transform_searcher.search_and_find_best_sequence(examples_to_learn_from, self.verbose)

    def apply(self, example):
        transformed_example, _ = self.transform_searcher.apply_transforms(self.chosen_transformations_, example)
        return transformed_example

    def show_transformations(self):
        print("Final sequence of transforms (cost={}):".format(self.best_cost_))
        for chosen_transformation in self.chosen_transformations_:
            print(chosen_transformation)

    def edit_cost(self, example1, example2):
        return self.transform_searcher.calculate_distance(example1, example2)

    def check_format_of_examples_to_learn_from(self, examples_to_learn_from):
        assert len(examples_to_learn_from) > 0
        for pair in examples_to_learn_from:
            assert len(pair) == 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('input_file', type=str, help='CSV file of mappings to learn')
    parser.add_argument('--verbose', default=False, action="store_true")
    args = parser.parse_args()

    verbose = args.verbose
    examples_to_learn_from = learner.load_examples(args.input_file)
    print("Loaded {} items from {}".format(len(examples_to_learn_from), args.input_file))

    transformer = Transformer(verbose)
    transformer.fit(examples_to_learn_from)

    transformer.show_transformations()

    print("\nTransformed versions of the input sequences:")
    for frm, to in examples_to_learn_from:
        transformed_frm = transformer.apply(frm)
        print("'{}'->'{}' compared to '{}' has distance '{}'".format(frm, transformed_frm, to, transformer.edit_cost(transformed_frm, to)))
