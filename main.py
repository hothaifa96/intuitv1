from flask import Flask, request, jsonify
from prometheus_client import Counter,Summary, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('request_counter','full requests counter',['method','endpoint','http_status'])
REQUEST_DURATION= Summary('request_duration_seconds','request duration',['method','endpoint'])

@app.route('/')
def Homepage():
    
    start_time = time.time()
    time.sleep(3)
    REQUEST_COUNT.labels(method='GET', endpoint='/',http_status=200).inc()
    end_time = time.time()
    REQUEST_DURATION.labels(method='GET',endpoint='/').observe(end_time - start_time)
    return "welcome to the flask demo hit the /ping endpoint please. "
    
@app.route('/ping', methods=['GET'])
def get_ip():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/ping',http_status=200).inc()
    ip_address = request.headers.get('X-Forwarded-For') or request.remote_addr
    end_time = time.time()
    REQUEST_DURATION.labels(method='GET',endpoint='/ping').observe(end_time - start_time)
    return jsonify({'message': 'pong', 'ip': ip_address})


@app.route('/metrics', methods=['GET'])
def metrics():
    return  generate_latest(),200,{'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
