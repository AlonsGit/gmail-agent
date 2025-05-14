import os
import json
from flask import Flask, request, jsonify
from send_email import send_email_with_attachment
from validate_email import is_valid_email
from summarize_tool import simple_summary

# Write GOOGLE_CREDENTIALS env content to temp file if needed
if os.getenv("GOOGLE_CREDENTIALS"):
    with open("/tmp/creds.json", "w") as f:
        f.write(os.getenv("GOOGLE_CREDENTIALS"))

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')
    attachment_path = data.get('attachment_path', None)

    message_id = send_email_with_attachment(
        creds_file="/tmp/creds.json",
        to=to,
        subject=subject,
        body=body,
        attachment_path=attachment_path
    )

    if message_id:
        return jsonify({"status": "success", "message_id": message_id})
    else:
        return jsonify({"status": "error"}), 500

@app.route('/validate_email', methods=['POST'])
def validate_email():
    data = request.json
    email = data.get('email')
    valid = is_valid_email(email)
    return jsonify({"valid": valid})

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get('text', '')
    summary = simple_summary(text)
    return jsonify({"summary": summary})

# ✅ נתיב ברירת מחדל עבור Render או בדיקת בריאות
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Email Agent API is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
