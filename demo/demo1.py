"""Annotate.io demo learning a transformation sequence for data cleaning"""
import requests
import argparse
import json

# Use case:
#
# You've got a set of data (the 'inputs') that you want to transform into a
# normalised form (the 'outputs'). You also have a much longer set of inputs
# that you'd like automatically normalised, based on the original training
# examples
#
# Usage:
#
# Call /learn with a POST call listing an array of 'inputs' and desired
# corresponding 'outputs'. The server will find the best possible
# transformation sequence as 'transforms'
#
# Call /transform with a POST with a longer list of 'inputs' and the same
# 'transforms', a new list of corresponding 'outputs' will be generated and
# returned
#
# Transforms used in this demo:
# Lowercase
# Strip white-space
# Convert unicode to ASCII
# Strip token (to remove 'Ltd')
# Fix badly encoded unicode

ROOT_URL = "http://api.annotate.io"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demo for api.annotate.io')
    parser.add_argument('--url', '-u', default=ROOT_URL, help='url for API')
    args = parser.parse_args()

    print("The header of this script contains notes that you should read!")

    # call / with a GET and confirm a 200 'OK' status code to confirm that the
    # site it running
    resp = requests.get(args.url)
    assert resp.status_code == 200

    # Use a POST to call /learn with examples of
    # the desired inputs and outputs
    url = args.url + "/learn"
    query = {'inputs': ['Accenture Ltd',
                        'Accenture Europe',
                        'Société Générale',
                        'SociÃ©tÃ© GÃ©nÃ©rale'],
             'outputs': ['accenture',
                         'accenture europe',
                         'societe generale',
                         'societe generale']}
    resp = requests.post(url,
                         data=json.dumps(query),
                         headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200
    print()
    print("Training phase (use inputs to learn a transformation to get to the desired outputs):")
    print("inputs:", query['inputs'])
    print("outputs:", query['outputs'])

    # store the code that we're sent
    transforms = resp.json()['transforms']

    # Use a POST to call /transform with the code
    # and new inputs, we'll receive outputs back
    url = args.url + "/transform"
    query = {'inputs': ['RBS Ltd',
                        'Royal Bank of Scotland Ltd',
                        'Lancôme',
                        ' Estée Lauder  '],
             'transforms': transforms}
    resp = requests.post(url,
                         data=json.dumps(query),
                         headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200

    print()
    print("Data cleaning phase (use the transformation sequence on inputs to generate new outputs):")
    print("inputs:", query['inputs'])
    print("outputs:", resp.json()['outputs'])
