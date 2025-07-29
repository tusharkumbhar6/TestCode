import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str
):
    # Create message container — the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Record the MIME types of both parts — text/plain and text/html.
    # You can also include a plain‑text version for older clients:
    text_body = "This is the fallback plain‑text message."
    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")

    # Attach parts into message container.
    # The email client will try the last part first.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via an SMTP server
    # Use SMTP_SSL for implicit TLS, or SMTP + starttls() for explicit.
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(username, password)
            server.sendmail(sender, recipients, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example usage:
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465
    USERNAME = "your.email@gmail.com"
    PASSWORD = "your-app-password"         # or OAuth2 token, etc.
    SENDER = "your.email@gmail.com"
    RECIPIENTS = ["friend1@example.com", "friend2@example.com"]
    SUBJECT = "🎉 Hello from Python (HTML Email)"
    HTML_BODY = """
    <html>
      <body>
        <h1 style="color: #1a73e8;">Hi there!</h1>
        <p>This is an <strong>HTML</strong> email sent from a Python script.</p>
        <p><a href="https://www.python.org">Learn more about Python</a></p>
      </body>
    </html>
    """

    send_html_email(
        SMTP_HOST, SMTP_PORT,
        USERNAME, PASSWORD,
        SENDER, RECIPIENTS,
        SUBJECT, HTML_BODY
    )
