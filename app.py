from flask import Flask, request, render_template
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json

byte_thresh = 20
rate_thresh = 40

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():

	if request.method == "POST":
		byte_thresh = int(request.form['byte'])
		rate_thresh = int(request.form['rate'])

	return render_template("index.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")


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
	
	byte_ave = 0
	rate_ave = 0

	entries = len(res['hits']['hits'])

	# Compute averages for byte length and data rate over all data
	for doc in res['hits']['hits']:

		if 'byte_length' in doc['_source']:
			byte_ave += doc['_source']['byte_length']
			rate_ave += doc['_source']['data_rate']

	results = {
		"code": 0
	}

	byte_ave /= entries
	rate_ave /= entries

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


