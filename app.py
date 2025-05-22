from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

FARE_RULES = load_json("data/fare_rules.json")
REGULATIONS = load_json("data/regulations.json")
AIRLINE_CODES = load_json("data/airlines.json")

@app.route('/')
def home():
    return jsonify({"message": "Aviation Dispute API v2 is running."})

@app.route('/airlines', methods=['GET'])
def get_airline_by_flight_id():
    flight_id = request.args.get('flight_id', '').upper()
    prefix = ''.join(filter(str.isalpha, flight_id))
    airline = AIRLINE_CODES.get(prefix)
    if airline:
        return jsonify({"airline": airline})
    return jsonify({"error": "Airline not found for this flight ID"}), 404

@app.route('/fare-rules', methods=['GET'])
def search_fare_rules():
    airline = request.args.get('airline', '').lower()
    keyword = request.args.get('keyword', '').lower()
    if airline in FARE_RULES:
        for fare_class, rules in FARE_RULES[airline].items():
            matched = {k: v for k, v in rules.items() if keyword in k.lower() or keyword in str(v).lower()}
            if matched:
                return jsonify({"airline": airline, "matches": matched})
    return jsonify({"error": "No matching rule found"}), 404

@app.route('/regulations', methods=['GET'])
def get_regulations():
    scope = request.args.get('scope', '').lower()
    keyword = request.args.get('keyword', '').lower()
    rules = REGULATIONS.get(scope, [])
    if keyword:
        rules = [r for r in rules if keyword in r['trigger'].lower() or keyword in r['entitlement'].lower()]
    if rules:
        return jsonify(rules)
    return jsonify({"error": "Regulations not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
