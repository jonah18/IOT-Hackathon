import random
import threading
import requests
from es_wrapper.general.formats import current_utc_time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def post(byte_lengths, rates, counter):
    host = 
    awsauth = 

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    result = {}
    result["byte_length"] = random.randint(byte_lengths[0], byte_lengths[1])
    result["sec_param"] = random.randint(0, 1)
    result["data_rate"] = random.randint(rates[0], rates[1])
    result["timestamp"] = current_utc_time()
    res = es.index(index="zigbee-index", doc_type='zigbee', id=counter, body=result)
    print(res['created'])


def get():
    threading.Timer(1, get).start()
    url = 'https://firehive.herokuapp.com/data'
    r = requests.get(url)
    # print r.content
    return r
    # will need to add functionality to respond to data...

get()


# call normal both
for x in range(30, 50):
    post((0, 20), (0, 40), x)
for x in range(50, 70):
    post((40, 60), (40, 80), x)
for x in range(70, 90):
    post((0, 20), (0, 40), x)
