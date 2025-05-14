
import os
import json
import traceback
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
    try:
        data = request.get_json(force=True)
        to = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        attachment_path = data.get('attachment_path', None)

        app.logger.info(f"Sending email to {to} with subject '{subject}'")

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
            return jsonify({"status": "error", "message": "Failed to send email"}), 500
    except Exception as e:
        traceback.print_exc()
        app.logger.error(f"Error in /send_email: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/validate_email', methods=['POST'])
def validate_email():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        app.logger.info(f"Validating email: {email}")
        valid = is_valid_email(email)
        return jsonify({"valid": valid})
    except Exception as e:
        traceback.print_exc()
        app.logger.error(f"Error in /validate_email: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        app.logger.info("Summarizing text")
        summary = simple_summary(text)
        return jsonify({"summary": summary})
    except Exception as e:
        traceback.print_exc()
        app.logger.error(f"Error in /summarize_text: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Email Agent API is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
