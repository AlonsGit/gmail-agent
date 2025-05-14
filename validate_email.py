import sys
import json
import smtplib
import dns.resolver
import socket
import re

def smtp_check(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)

        server = smtplib.SMTP(timeout=5)
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(socket.gethostname())
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False
    return smtp_check(email)

if __name__ == '__main__':
    inputs = json.load(sys.stdin)
    email = inputs.get("email")
    result = is_valid_email(email)
    print(json.dumps({"valid": result}))
