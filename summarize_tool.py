# email_agent_api.py
from flask import Flask, request, jsonify
from summarize_tool import simple_summary

app = Flask(__name__)

@app.route('/summarize_text', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    summary = simple_summary(text)
    return jsonify({"summary": summary})
