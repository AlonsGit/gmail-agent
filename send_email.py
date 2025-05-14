import base64
import os
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

def send_email_with_attachment(creds_file, to, subject, body, attachment_path=None):
    creds = Credentials.from_authorized_user_file(creds_file, ['https://www.googleapis.com/auth/gmail.send'])
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    if attachment_path:
        filename = os.path.basename(attachment_path)
        if not os.path.isfile(attachment_path):
            raise FileNotFoundError(f"Attachment not found: {attachment_path}")
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': raw}

    sent_message = service.users().messages().send(userId='me', body=create_message).execute()
    return sent_message['id']

@app.route('/send_email', methods=['POST'])
def send_email_api():
    try:
        data = request.get_json()
        to = data['to']
        subject = data['subject']
        body = data['body']
        attachment_path = data.get('attachment_path', None)

        creds_file = 'credentials.json'
        message_id = send_email_with_attachment(creds_file, to, subject, body, attachment_path)

        return jsonify({'status': 'success', 'message_id': message_id}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
