import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 1) build the root multipart/mixed container
msg = MIMEMultipart("mixed")
msg["Subject"] = "Test Email with Base64 PNG"
msg["From"]    = "me@domain.com"
msg["To"]      = "you@domain.com"

# 2) add your HTML part that references the CID
html = """\
<html>
  <body>
    <h1>Logo Below</h1>
    <img src="cid:mylog.png" alt="Logo">
  </body>
</html>
"""
msg.attach(MIMEText(html, "html"))

# 3) read and attach the image as base64
with open("mylog.png", "rb") as f:
    img_data = f.read()

img_part = MIMEBase("image", "png", name=os.path.basename("mylog.png"))
img_part.set_payload(img_data)
encoders.encode_base64(img_part)

# set the headers exactly as you showed
img_part.add_header("Content-ID", "<mylog.png>")
img_part.add_header("Content-Disposition", "attachment", filename="mylog.png")

msg.attach(img_part)

# 4) send via SMTP
with smtplib.SMTP("localhost", 25) as s:
    s.send_message(msg)
