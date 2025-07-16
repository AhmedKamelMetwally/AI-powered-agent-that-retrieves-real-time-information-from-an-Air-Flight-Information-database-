from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key from environment variable
api_key = os.getenv("LANGFLOW_API_KEY")
if not api_key:
    raise EnvironmentError("LANGFLOW_API_KEY environment variable not found.")

# Langflow API endpoint
LANGFLOW_API_URL = "http://localhost:7860/api/v1/run/airline-agent"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    # Construct payload
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": data["message"]
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    try:
        # Make request to Langflow API
        response = requests.post(LANGFLOW_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 502


# Health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
