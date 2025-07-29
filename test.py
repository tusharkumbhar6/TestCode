import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_base64_attachments(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    image_path: str,
    text_path: str
):
    # 1) Root container: multipart/mixed
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = ", ".join(recipients)

    # 2) HTML part
    msg.attach(MIMEText(html_body, "html"))

    # 3) Image as base64 attachment with full headers
    with open(image_path, "rb") as img_fp:
        img_data = img_fp.read()
    img_part = MIMEBase("image", "png", name=os.path.basename(image_path))
    img_part.set_payload(img_data)
    encoders.encode_base64(img_part)
    img_part.add_header("Content-Type", f'image/png; name="{os.path.basename(image_path)}"')
    img_part.add_header("Content-Transfer-Encoding", "base64")
    img_part.add_header("Content-ID", f'<{os.path.basename(image_path)}>')
    img_part.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(image_path)}"'
    )
    msg.attach(img_part)

    # 4) Text file as base64 attachment with headers
    with open(text_path, "rb") as txt_fp:
        txt_data = txt_fp.read()
    txt_part = MIMEBase("text", "plain", name=os.path.basename(text_path))
    txt_part.set_payload(txt_data)
    encoders.encode_base64(txt_part)
    txt_part.add_header("Content-Type", f'text/plain; name="{os.path.basename(text_path)}"')
    txt_part.add_header("Content-Transfer-Encoding", "base64")
    txt_part.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(text_path)}"'
    )
    msg.attach(txt_part)

    # 5) Send the email (no auth)
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, recipients, msg.as_string())
        print("Email sent with base64 attachments!")

if __name__ == "__main__":
    HTML = """
    <html><body>
      <h1>Here’s our logo & attachment:</h1>
      <p>The PNG below is sent as a base64 part; it won’t render inline, but can be downloaded.</p>
    </body></html>
    """
    send_email_with_base64_attachments(
        smtp_host="localhost",
        smtp_port=25,
        sender="you@domain.com",
        recipients=["friend@example.com"],
        subject="Test: Base64 Attachments",
        html_body=HTML,
        image_path="mylog.png",
        text_path="info.txt"
    )
