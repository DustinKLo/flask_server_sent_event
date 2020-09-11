import random
import time
import json
import uuid

from pprint import pprint

from flask import Flask, Response, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


def generate_event_source_data(d):
	json_str = json.dumps(d)
	return 'data: %s\n\n' % json_str


def event_stream():
	for i in range(40):
		_id = uuid.uuid4()
		time.sleep(random.uniform(0, 0.2))
		data = {
			'id': str(_id),
			'message': 'Data pushed from server: (%d)' % (i + 1),
		}
		app.logger.debug(data)
		yield generate_event_source_data(data)


@app.route('/stream')
def stream():
	app.logger.info(request.args)
	resp = Response(event_stream(), mimetype="text/event-stream")
	resp.headers['Cache-Control'] = 'no-cache'
	resp.headers["Access-Control-Allow-Origin"] = "*"
	resp.headers['Content-Type'] = 'text/event-stream'
	return resp


@app.route('/api/test')
def test():
	pprint(request.environ)
	return jsonify({
		'hello': 'world!'
	})


@app.route('/')
def home():
	return render_template('./index.html', template_folder='templates')


if __name__ == '__main__':
	app.run(debug=True)  # threaded=True
