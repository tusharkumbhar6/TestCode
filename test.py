import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_html_email_no_auth(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str
):
    # Create the container (multipart/alternative)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Attach the HTML part
    html_part = MIMEText(html_body, "html")
    msg.attach(html_part)

    # Send via SMTP without logging in
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, recipients, msg.as_string())
        print("Email sent (no auth).")

if __name__ == "__main__":
    send_html_email_no_auth(
        smtp_host="localhost",
        smtp_port=25,
        sender="you@yourdomain.com",
        recipients=["friend@example.com"],
        subject="Hello from Python (HTML!)",
        html_body="""
        <html>
          <body>
            <h1 style="color: #2e6c80;">Hi there!</h1>
            <p>This is an <strong>HTML</strong> email without auth.</p>
          </body>
        </html>
        """
    )
