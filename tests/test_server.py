"""Tests for the Flask server"""
import unittest
import json
from learning_text_transformer import server

IN_OUT_1 = {'inputs': [], 'outputs': []}, 200
IN_OUT_2 = {'inputs': ['Company1 Ltd'], 'outputs': ['company1']}, 200
IN_OUT_3 = {'inputs': ['1 item'], 'outputs': []}, 400


# why don't i get .get_json() on my resp items?

class TestServerLearn(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def test_get_home(self):
        self.app.get('/')

    def test_post_learn_no_items(self):
        resp = self.app.post('/learn', data=json.dumps(IN_OUT_1[0]), headers=[('Content-Type', 'application/json')])
        self.assertEqual(resp.status_code, IN_OUT_1[1])

    def test_post_learn_unequal_items(self):
        resp = self.app.post('/learn', data=json.dumps(IN_OUT_3[0]), headers=[('Content-Type', 'application/json')])
        self.assertEqual(resp.status_code, IN_OUT_3[1])

    def test_post_learn_1_item(self):
        resp = self.app.post('/learn', data=json.dumps(IN_OUT_2[0]), headers=[('Content-Type', 'application/json')])
        out = json.loads(str(resp.data, "utf-8"))
        print("Received back:", out)
        self.assertEqual(resp.status_code, IN_OUT_2[1])

        ts = out['transforms']
        self.assertEqual(len(ts), 3)


class TestServerLearnTransform(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def convert_and_post(self, path, data_dict):
        resp = self.app.post(path, data=json.dumps(data_dict), headers=[('Content-Type', 'application/json')])
        return resp

    def test_post_learn_1_item(self):
        resp = self.convert_and_post('/learn', IN_OUT_2[0])
        out = json.loads(str(resp.data, "utf-8"))
        self.assertEqual(resp.status_code, IN_OUT_2[1])

        ts = out['transforms']
        self.assertEqual(len(ts), 3)

        # call /transform with data transforms=lst, froms=lst
        # get tos as a list back

        out['inputs'] = ['an input Ltd']
        resp = self.convert_and_post('/transform', out)
        out = json.loads(str(resp.data, "utf-8"))
        expected = {'outputs': ['an input']}
        self.assertEqual(out, expected)
        print(out)
