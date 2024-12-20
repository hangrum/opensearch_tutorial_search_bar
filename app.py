from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # CORS 활성화

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    data = request.json
    query = data.get("query")

    # 쿼리 값 확인
    if not query or not isinstance(query, str):
        return jsonify({"error": "Invalid query parameter"}), 400

    url = "http://127.0.0.1:9200/opensearch_dashboards_sample_data_flights/_search"
    auth = ("admin", "ChangeTh1sPassW@rd")
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": {
            "bool": {
                "should": [
                    {"wildcard": {"Dest": f"*{query}*"}},
                    {"wildcard": {"Origin": f"*{query}*"}},
                    {"wildcard": {"DestCountry": f"*{query}*"}},
                    {"wildcard": {"OriginCountry": f"*{query}*"}},
                    {"wildcard": {"DestCityName": f"*{query}*"}},
                    {"wildcard": {"OriginCityName": f"*{query}*"}}
                ]
            }
        }
    }

    try:
        response = requests.post(url, json=payload, auth=auth, headers=headers)
        print(f"Request sent to: {url}")
        print(f"Payload: {payload}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        response.raise_for_status()

        hits = response.json().get("hits", {}).get("hits", [])
        if hits:
            return jsonify(hits)
        else:
            return jsonify({"error": "No results found"}), 404

    except requests.exceptions.RequestException as e:
        print(f"OpenSearch Error: {e}")
        return jsonify({"error": "OpenSearch 에러"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=60022)

