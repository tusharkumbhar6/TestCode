import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email_with_image(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    sender: str,
    recipients: list[str],
    subject: str,
    html_body: str,
    image_path: str,
    cid_name: str = "inline_image"
):
    # --- Build the Email ---
    # Use a “related” multipart so we can embed images inline
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Alternative part for HTML (and fallback plain‑text if you want)
    alt = MIMEMultipart("alternative")
    msg.attach(alt)

    # Plain‑text fallback
    alt.attach(MIMEText("This email contains an image. Please view in an HTML‑capable client.", "plain"))

    # HTML part referencing our image by CID
    html = f"""
    <html>
      <body>
        {html_body}
        <p><img src="cid:{cid_name}" alt="embedded image"></p>
      </body>
    </html>
    """
    alt.attach(MIMEText(html, "html"))

    # Read the image file and attach it
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()

    img = MIMEImage(img_data, _subtype=os.path.splitext(image_path)[1][1:])
    # Give it the Content‑ID we referenced in our HTML
    img.add_header("Content-ID", f"<{cid_name}>")
    # (optional) also set filename if you want it as an attachment
    img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
    msg.attach(img)

    # --- Send it ---
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(username, password)
        server.send_message(msg)

if __name__ == "__main__":
    send_email_with_image(
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        username="your.email@gmail.com",
        password="your-app-password",
        sender="your.email@gmail.com",
        recipients=["friend@example.com"],
        subject="Here's a cool picture!",
        html_body="<h1>Check out this PNG</h1>",
        image_path="path/to/your/image.png",
        cid_name="my_png_cid"
    )
