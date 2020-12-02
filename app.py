import random
import time
import json
import uuid

import subprocess

from pprint import pprint

from flask import Flask, Response, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


def generate_event_source_data(d):
	json_str = json.dumps(d)
	return 'data: %s\n\n' % json_str


@app.route('/stream')
def stream():
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

	app.logger.info(request.args)
	resp = Response(event_stream(), mimetype="text/event-stream")
	resp.headers['Cache-Control'] = 'no-cache'
	resp.headers["Access-Control-Allow-Origin"] = "*"
	resp.headers['Content-Type'] = 'text/event-stream'
	return resp


@app.route('/stdout')
def stream_bash_stdout():
	def execute():
		cmd = 'for i in {1..10}; do echo "count: $i"; sleep 0.5; done;'
		popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
		for stdout_line in iter(popen.stdout.readline, ""):
			app.logger.debug(stdout_line)
			yield 'data: ' + stdout_line + '\n'
		popen.stdout.close()

	resp = Response(execute(), mimetype="text/event-stream")
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
