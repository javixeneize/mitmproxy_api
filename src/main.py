from mitmproxy_api import mitmproxy_api
from flask import Flask, request, Response
import json

app = Flask(__name__)


@app.route('/getUrlCodeAndHeaders', methods=['POST'])
@app.route('/getPostUrlsAndBody', methods=['POST'])
@app.route('/getFolders', methods=['POST'])
def getData():
    try:
        data = request.json
        m = mitmproxy_api(data['domain'], data['file'])
        m.getDataFile()
        endpoint = str(request.url_rule)[1:]
        method = (getattr(m, endpoint))
        return (json.dumps(method()))
    except KeyError as e:
        error = {}
        error['Error'] = "Key {} not found".format(e)
        return Response(json.dumps(error), status=500, mimetype="application/json")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
