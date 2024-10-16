import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def send_email_with_attachment(to_email, subject, body, attachment_path):
    from_email = "your_email@example.com"  # Replace with your email
    password = "your_email_password"  # Replace with your email password

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body and the file
    msg.attach(MIMEText(body, 'plain'))
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
    msg.attach(part)

    # Send the email
    with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

# Usage
if __name__ == "__main__":
    send_email_with_attachment("recipient@example.com", "Your Subject", "Email body text.", "executive_summary.pdf")
