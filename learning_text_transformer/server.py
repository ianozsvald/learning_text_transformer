"""Flask server"""

from flask import Flask, request, jsonify
from flask.ext import restful
from flask.ext.restful import abort
from learning_text_transformer import learner3 as learner
from learning_text_transformer import transforms

app = Flask(__name__)
api = restful.Api(app)



def log_learn_entry(examples_to_learn_from):
    pass

def log_learn_exit(result, best_score):
    pass

def log_transform_entry(inputs):
    pass


class HelloWorld(restful.Resource):
    def get(self):
        return {'learning': 'server'}
api.add_resource(HelloWorld, '/')


def make_learn_result(ts):
    serialisation = transforms.Serialisation()
    serialised_json = serialisation.serialise(ts)
    result = {"transforms": serialised_json}
    return result


class Learn(restful.Resource):
    def check_inputs_or_abort(self, reqs):
        if len(reqs['inputs']) != len(reqs['outputs']):
            abort(400)

    def post(self):
        reqs = request.get_json()
        print("reqs:", reqs)
        self.check_inputs_or_abort(reqs)
        examples_to_learn_from = list(zip(reqs['inputs'], reqs['outputs']))
        log_learn_entry(examples_to_learn_from)
        best_score = None
        if examples_to_learn_from:
            transform_searcher = learner.get_transform_searcher()
            chosen_transformations, best_score = transform_searcher.search_and_find_best_sequence(examples_to_learn_from)
        else:
            chosen_transformations = []
        result = make_learn_result(chosen_transformations)
        log_learn_exit(result, best_score)
        return jsonify(result)
api.add_resource(Learn, '/learn')


class Transform(restful.Resource):
    def post(self):
        reqs = request.get_json()
        serialisation = transforms.Serialisation()
        inputs = reqs['inputs']
        #log_transform_entry(inputs)
        outputs = []
        for s in inputs:
            ts_raw = reqs['transforms']
            ts = serialisation.deserialise(ts_raw)
            transform_searcher = learner.get_transform_searcher()
            result, transform_always_made_changes = transform_searcher.apply_transforms(ts, s)
            outputs.append(result)

        result = {'outputs': outputs}
        return jsonify(result)
api.add_resource(Transform, '/transform')


if __name__ == '__main__':
    app.run(debug=True)
