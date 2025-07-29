import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

def send_html_email_with_logo_and_txt(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    logo_path: str,
    text_file_path: str,
    logo_cid: str = "logo_cid"
):
    # -- Root container (mixed) to hold everything --
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # -- Build the body as “related” to allow inline images --
    related = MIMEMultipart("related")
    msg.attach(related)

    # Alternative part for plaintext + HTML
    alternative = MIMEMultipart("alternative")
    related.attach(alternative)

    # 1) Plain‑text fallback
    alternative.attach(MIMEText("This email contains HTML, an inline logo, and a text attachment.", "plain"))

    # 2) HTML part, referencing the logo via its CID
    #    Make sure your html_body includes something like: <img src="cid:logo_cid">
    html_with_logo = f"""
    <html>
      <body>
        {html_body}
        <p><img src="cid:{logo_cid}" alt="Logo"></p>
      </body>
    </html>
    """
    alternative.attach(MIMEText(html_with_logo, "html"))

    # -- Attach the inline logo image --
    with open(logo_path, "rb") as img_file:
        img_data = img_file.read()
    subtype = os.path.splitext(logo_path)[1].lstrip(".") or "png"
    img = MIMEImage(img_data, _subtype=subtype)
    img.add_header("Content-ID", f"<{logo_cid}>")
    img.add_header("Content-Disposition", "inline", filename=os.path.basename(logo_path))
    related.attach(img)

    # -- Attach the text file as a regular attachment --
    with open(text_file_path, "rb") as txt_file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(txt_file.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment",
        filename=os.path.basename(text_file_path)
    )
    msg.attach(part)

    # -- Send via SMTP (no auth) --
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, recipients, msg.as_string())
        print("Email sent with inline logo and text attachment!")

if __name__ == "__main__":
    send_html_email_with_logo_and_txt(
        smtp_host="localhost",
        smtp_port=25,
        sender="you@yourdomain.com",
        recipients=["friend@example.com"],
        subject="HTML Email with Logo + Text File",
        html_body="<h1>Greetings!</h1><p>Here’s our company logo below.</p>",
        logo_path="path/to/logo.png",
        text_file_path="path/to/info.txt"
    )
