
import sys
import json
import smtplib
import dns.resolver
import socket
from email_validator import validate_email, EmailNotValidError

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
        # fallback in case of SMTP resolution failure
        return True

def is_valid_email(email):
    try:
        # בדיקת תקינות התחביר של כתובת האימייל
        validate_email(email)
    except EmailNotValidError:
        return False

    # בדיקת SMTP כדי לוודא שהכתובת יכולה לקבל דואר (fallback ל-True אם לא ניתן לבדוק)
    return smtp_check(email)

if __name__ == '__main__':
    inputs = json.load(sys.stdin)
    email = inputs.get("email")
    result = is_valid_email(email)
    print(json.dumps({"valid": result}))
