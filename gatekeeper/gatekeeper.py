import argparse
import re
import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("proxy_private_dns", help="Private dns to reach the proxy")
args = parser.parse_args()

proxy_private_dns = args.proxy_private_dns

select_validator = re.compile(r"(?i)(^SELECT \* FROM actor .)")
insert_validator = re.compile(r"(?i)(^INSERT INTO actor ?\((first_name,\s{0,}last_name)\) VALUES)")

def validate_query(type, query):
    if type == "select":
        if select_validator.match(" ".join(query.split())):
            return True
        else:
            return False
    elif type == "insert":
        if insert_validator.match(" ".join(query.split())):
            return True
        else:
            return False
    else:
        return False
    
@app.route("/direct", methods=["POST"])
def direct_post():
    request_data = request.get_json()
    query = request_data['query']
    if validate_query("insert", query):
        response = requests.post("http://" + proxy_private_dns + ":8080/direct", json=request_data)
        return json.loads(response.content)
    else:
        return jsonify(message="Access denied by gatekeeper"), 403
    
@app.route("/direct", methods=["GET"])
def direct_get():
    request_data = request.get_json()
    query = request_data['query']
    if validate_query("select", query):
        response = requests.get("http://" + proxy_private_dns + ":8080/direct", json=request_data)
        return json.loads(response.content)
    else:
        return jsonify(message="Access denied by gatekeeper"), 403
    
@app.route("/random", methods=["GET"])
def random_get():
    request_data = request.get_json()
    query = request_data['query']
    if validate_query("select", query):
        response = requests.get("http://" + proxy_private_dns + ":8080/random", json=request_data)
        return json.loads(response.content)
    else:
        return jsonify(message="Access denied by gatekeeper"), 403
    
@app.route("/custom", methods=["GET"])
def custom_get():
    request_data = request.get_json()
    query = request_data['query']
    if validate_query("select", query):
        response = requests.get("http://" + proxy_private_dns + ":8080/custom", json=request_data)
        return json.loads(response.content)
    else:
        return jsonify(message="Access denied by gatekeeper"), 403

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
