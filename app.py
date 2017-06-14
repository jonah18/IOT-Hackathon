from flask import Flask
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

app = Flask(__name__)

@app.route('/')
def index():
	host = 'search-houseshark-ixotnqxkzathhe3en6ql2egzha.us-east-1.es.amazonaws.com'
    awsauth = AWS4Auth('AKIAI7S7SHF547UFU5MA', '1tm6QTj6EgNy5lx//F3IHwmkSoaVBtzEuaqh+Yu6', 'us-east-1', 'es')

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    res = es.get(index="zigbee-index", doc_type='zigbee')
	print(res['_source'])


    return res

if __name__ == "__main__":
    app.run()
