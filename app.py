from flask import Flask
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json

app = Flask(__name__)

@app.route("/")
def index():
	return "Welcome"

@app.route('/data')
def data():
	host = 'search-houseshark-ixotnqxkzathhe3en6ql2egzha.us-east-1.es.amazonaws.com'
	awsauth = AWS4Auth('AKIAI7S7SHF547UFU5MA', '1tm6QTj6EgNy5lx//F3IHwmkSoaVBtzEuaqh+Yu6', 'us-east-1', 'es')

	es = Elasticsearch(
		hosts=[{'host': host, 'port': 443}],
		http_auth=awsauth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
	)

	res = es.search(index="zigbee-index", doc_type="zigbee", body={"query": {"match_all": {}}})

	byte_thresh = 20
	rate_thresh = 40
	
	byte_ave = 0
	rate_ave = 0

	entries = len(res['hits']['hits'])

	# Compute averages for byte length and data rate over all data
	for doc in res['hits']['hits']:
		byte_ave += doc['_source']['byte_length']
		rate_ave += doc['_source']['data_rate']

	byte_ave /= entries
	rate_ave /= entries

	results = {
		"code": 0
	}

	if rate_ave > rate_thresh:
		results['code'] = 1


	"""
	Codes:
		0 - All good
		1 - Data rate too high
	"""

	return json.dumps(results)

if __name__ == "__main__":
    app.run(threaded=True)


