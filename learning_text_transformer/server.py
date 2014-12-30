"""Flask server"""

from flask import Flask, request
from flask.ext import restful
from flask.ext.restful import abort
import json
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
    result = {"transforms": json.loads(serialised_json)}
    return result


class Learn(restful.Resource):
    def check_inputs_or_abort(self, reqs):
        if len(reqs['from']) == 0:
            abort(400)

    def post(self):
        reqs = request.get_json()
        #examples_to_learn_from = [(reqs['from'][0], reqs['to'][0])]
        print("reqs:", reqs)
        self.check_inputs_or_abort(reqs)
        examples_to_learn_from = list(zip(reqs['from'], reqs['to']))
        chosen_transformations, best_score = learner.search_and_find_best_sequence(examples_to_learn_from)
        result = make_learn_result(chosen_transformations)
        return result
api.add_resource(Learn, '/learn')


if __name__ == '__main__':
    app.run()
