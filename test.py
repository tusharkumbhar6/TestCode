from email import message_from_string, policy
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser

# 1. Parse your raw email (bytes or str) into a Message object
raw_email = """\
From: alice@example.com
To: bob@example.com
Subject: Hi there!
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============123456789=="

--===============123456789==
Content-Type: text/plain; charset="utf-8"

Hello Bob, this is the plain‑text part.

--===============123456789==
Content-Type: text/html; charset="utf-8"

<html><body><p>Hello Bob, <strong>this</strong> is HTML!</p></body></html>

--===============123456789==
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="example.txt"
Content-Transfer-Encoding: base64

SGVsbG8sIHRoaXMgYSB0ZXN0IGZpbGUuCg==

--===============123456789==--
"""
msg: EmailMessage = message_from_string(raw_email, policy=policy.default)

# 2. Grab all headers
print("Headers:")
for name, value in msg.items():
    print(f"  {name}: {value}")

# 3. If it’s multipart, walk through each part
print("\nBody & Attachments:")
for part in msg.walk():
    ctype = part.get_content_type()
    cdisp = part.get_content_disposition()  # 'inline', 'attachment', or None

    # skip container parts
    if part.is_multipart():
        continue

    # attachments
    if cdisp == 'attachment':
        fname = part.get_filename()
        payload = part.get_payload(decode=True)  # bytes
        print(f"  Attachment — {fname} ({len(payload)} bytes)")

    # inline text
    elif ctype == 'text/plain':
        text = part.get_content()
        print("  Plain text body:")
        print(text)

    elif ctype == 'text/html':
        html = part.get_content()
        print("  HTML body:")
        print(html)

    else:
        # any other content (images, non‑text, etc.)
        data = part.get_payload(decode=True)
        print(f"  Other part: {ctype}, {len(data)} bytes")

# 4. If it isn’t multipart, it’s just a single payload:
if not msg.is_multipart():
    body = msg.get_content()
    print("\nSingle-part body:")
    print(body)

def print_attachments(raw_email_bytes):
    # Parse the raw email into an EmailMessage
    msg = BytesParser(policy=policy.default).parsebytes(raw_email_bytes)

    # Walk through the parts looking for attachments
    for part in msg.iter_attachments():
        filename = part.get_filename() or "<no name>"
        payload = part.get_payload(decode=True)  # always returns bytes

        print(f"\nAttachment: {filename}")
        print("-" * (11 + len(filename)))

        # Try to decode as UTF‑8 text if it’s a text/* subtype
        maintype, subtype = part.get_content_type().split("/")
        if maintype == "text":
            try:
                text = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                print(text)
            except Exception as e:
                print(f"[!] Could not decode text: {e}")
        else:
            # For non-text attachments, show a hex preview (first 100 bytes)
            preview = payload[:100].hex()
            print(f"[binary data, {len(payload)} bytes] preview (hex):")
            print(preview + ("…" if len(payload) > 100 else ""))

raw_bytes = raw_email.encode("utf-8")
print_attachments(raw_bytes)
