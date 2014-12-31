"""Flask server"""

from flask import Flask, request, jsonify
from flask.ext import restful
from flask.ext.restful import abort
from learning_text_transformer import learner3 as learner
from learning_text_transformer import transforms

app = Flask(__name__)
api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return {'nothing': 'here'}
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
        if examples_to_learn_from:
            chosen_transformations, best_score = learner.search_and_find_best_sequence(examples_to_learn_from)
        else:
            chosen_transformations = []
        result = make_learn_result(chosen_transformations)
        return jsonify(result)
api.add_resource(Learn, '/learn')


class Transform(restful.Resource):
    def post(self):
        reqs = request.get_json()
        serialisation = transforms.Serialisation()
        inputs = reqs['inputs']
        outputs = []
        for s in inputs:
            ts_raw = reqs['transforms']
            ts = serialisation.deserialise(ts_raw)
            result = learner.apply_transforms(ts, s)
            outputs.append(result)

        result = {'outputs': outputs}
        return jsonify(result)
api.add_resource(Transform, '/transform')


if __name__ == '__main__':
    app.run(debug=True)
