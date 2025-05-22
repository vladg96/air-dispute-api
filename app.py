from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

FARE_RULES = load_json("data/fare_rules.json")
REGULATIONS = load_json("data/regulations.json")

@app.route('/')
def home():
    return jsonify({"message": "Aviation Dispute API is running."})

@app.route('/fare-rules', methods=['GET'])
def get_fare_rules():
    airline = request.args.get('airline', '').lower()
    fare_class = request.args.get('fare_class', '').lower()
    if airline in FARE_RULES and fare_class in FARE_RULES[airline]:
        return jsonify(FARE_RULES[airline][fare_class])
    return jsonify({"error": "Fare data not found"}), 404

@app.route('/regulations', methods=['GET'])
def get_regulations():
    scope = request.args.get('scope', '').lower()
    keyword = request.args.get('keyword', '').lower()
    rules = REGULATIONS.get(scope, [])
    if keyword:
        rules = [r for r in rules if keyword in r['trigger'].lower()]
    if rules:
        return jsonify(rules)
    return jsonify({"error": "Regulations not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
