from flask import Flask, request, session

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=['GET'])
def run_server():


    resp = None
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
