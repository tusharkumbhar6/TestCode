import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_inline_image_and_text_attachment(
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

    # 2) Related container for HTML + inline image
    related = MIMEMultipart("related")
    msg.attach(related)

    # 3) HTML part (must reference the CID you’ll set below)
    #    e.g. <img src="cid:mylog.png">
    html_part = MIMEText(html_body, "html")
    related.attach(html_part)

    # 4) Inline PNG as a base64‐encoded part with Content-ID
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as img_fp:
        img_data = img_fp.read()
    img_part = MIMEBase("image", "png", name=filename)
    img_part.set_payload(img_data)
    encoders.encode_base64(img_part)
    img_part.add_header("Content-Type",    f'image/png; name="{filename}"')
    img_part.add_header("Content-Transfer-Encoding", "base64")
    img_part.add_header("Content-ID",      f'<{filename}>')
    img_part.add_header("Content-Disposition", f'inline; filename="{filename}"')
    related.attach(img_part)

    # 5) Text file attachment (still base64‐encoded)
    txt_name = os.path.basename(text_path)
    with open(text_path, "rb") as txt_fp:
        txt_data = txt_fp.read()
    txt_part = MIMEBase("text", "plain", name=txt_name)
    txt_part.set_payload(txt_data)
    encoders.encode_base64(txt_part)
    txt_part.add_header("Content-Type",    f'text/plain; name="{txt_name}"')
    txt_part.add_header("Content-Transfer-Encoding", "base64")
    txt_part.add_header("Content-Disposition",  f'attachment; filename="{txt_name}"')
    msg.attach(txt_part)

    # 6) Send via SMTP (no auth)
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, recipients, msg.as_string())
        print("Email sent with inline image and text file attachment!")

if __name__ == "__main__":
    HTML = """
<html>
  <body>
    <h1>Here’s our inline logo:</h1>
    <p><img src="cid:mylog.png" alt="Logo"></p>
    <p>And a text file is attached below.</p>
  </body>
</html>
"""
    send_email_with_inline_image_and_text_attachment(
        smtp_host="localhost",
        smtp_port=25,
        sender="you@domain.com",
        recipients=["friend@example.com"],
        subject="Inline Logo + Text Attachment",
        html_body=HTML,
        image_path="mylog.png",
        text_path="info.txt"
    )
