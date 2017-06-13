import random
import threading.Timer
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def post(byterange, raterange):
    host = 'search-houseshark-ixotnqxkzathhe3en6ql2egzha.us-east-1.es.amazonaws.com'
    awsauth = AWS4Auth('AKIAI7S7SHF547UFU5MA', '1tm6QTj6EgNy5lx//F3IHwmkSoaVBtzEuaqh+Yu6', 'us-east-1', 'es')

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    result = {}
    result["byte_length"] = random.randint(0, byterange)
    result["sec_param"] = random.randint(0, 1)
    result["data_rate"] = random.randint(0, raterange)

    counter = 10
    res = es.index(index="test-index", doc_type='zigbee', id=counter, body=result)
    counter += 1
    print(res['created'])


def get():
    url = ''
    r = requests.get(url)
    return r

# call high byte length post
# post(50, 10)

# call high rate range
# post(10, 50)

# call high both
# post(50, 50)

t = threading.Timer(1, get)
t.start()

# call normal both
for x in range(0, 10):
    post(10, 10)
