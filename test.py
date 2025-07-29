import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email_with_image_no_auth(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    image_path: str,
    cid_name: str = "inline_image"
):
    # Build the email as “related” so images can be embedded
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Alternative part for plain‑text + HTML
    alt = MIMEMultipart("alternative")
    msg.attach(alt)
    alt.attach(MIMEText("This email contains an image. View in HTML‑capable client.", "plain"))
    html = f"""
    <html>
      <body>
        {html_body}
        <p><img src="cid:{cid_name}" alt="embedded image"></p>
      </body>
    </html>
    """
    alt.attach(MIMEText(html, "html"))

    # Attach the PNG
    with open(image_path, "rb") as f:
        img_data = f.read()
    subtype = os.path.splitext(image_path)[1].lstrip(".") or "png"
    img = MIMEImage(img_data, _subtype=subtype)
    img.add_header("Content-ID", f"<{cid_name}>")
    img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
    msg.attach(img)

    # Send without login
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.send_message(msg)
        print("Email sent (no auth).")

if __name__ == "__main__":
    send_email_with_image_no_auth(
        smtp_host="localhost",
        smtp_port=25,
        sender="me@mydomain.com",
        recipients=["friend@example.com"],
        subject="Here’s a PNG, no auth!",
        html_body="<h1>Inline PNG test</h1>",
        image
