import requests
import argparse
import json

ROOT_URL = "http://api.annotate.io"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--url', '-u', default=ROOT_URL, help='url for API')
    args = parser.parse_args()
    print("Using root URL:", args.url)

    print("GET /", requests.get(args.url).json())
    print("POST /", requests.post(args.url).text)

    url = args.url + "/learn"
    query = {'inputs': ['Accenture Ltd', 'accenture Europe'],
             'outputs': ['accenture', 'accenture europe']}
    resp = requests.get(url,
                         data=json.dumps(query),
                         headers={'Content-Type': 'application/json'})
    print(resp.status_code)
    print(resp.text)
    print(resp.json())


    resp = requests.post(url,
                         data=json.dumps(query),
                         headers={'Content-Type': 'application/json'})
    print(resp.status_code)
    print(resp.text)
    print(resp.json())
