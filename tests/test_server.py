"""Tests for the Flask server"""
import unittest
import json
from learning_text_transformer import server

IN_OUT_1 = {'from': [], 'to': []}, 400
IN_OUT_2 = {'from': ['Company1 Ltd'], 'to': ['company1']}, 200


class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def test_get_home(self):
        self.app.get('/')

    def test_post_learn_no_items(self):
        resp = self.app.post('/learn', data=json.dumps(IN_OUT_1[0]), headers=[('Content-Type', 'application/json')])
        self.assertEqual(resp.status_code, IN_OUT_1[1])

    def test_post_learn_1_item(self):
        resp = self.app.post('/learn', data=json.dumps(IN_OUT_2[0]), headers=[('Content-Type', 'application/json')])
        out = json.loads(str(resp.data, "utf-8"))
        print("Received back:", out)
        self.assertEqual(resp.status_code, IN_OUT_2[1])

        ts = out['transforms']
        self.assertEqual(len(ts), 3)

        # call /transform with data transforms=lst, froms=lst
        # get tos as a list back
