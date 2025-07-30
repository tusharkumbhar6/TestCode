#!/usr/bin/env python3
import sys
import smtplib
from email import policy
from email.parser import BytesParser

def send_eml(
    eml_path: str,
    smtp_host: str,
    smtp_port: int = 25,
    use_tls: bool = False
):
    """
    Read a .eml file and send it via SMTP without logging in.
    
    :param eml_path: Path to the .eml file
    :param smtp_host: SMTP server hostname or IP
    :param smtp_port: SMTP port (default 25)
    :param use_tls: If True, will do STARTTLS()
    """
    # 1) Parse the .eml file into an EmailMessage
    with open(eml_path, "rb") as fp:
        msg = BytesParser(policy=policy.SMTP).parse(fp)

    # 2) Connect to SMTP
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.set_debuglevel(1)      # shows SMTP session; set to 0 to silence
        if use_tls:
            server.starttls()

        # 3) Send the message exactly as parsed
        server.send_message(msg)

    print(f"Sent `{eml_path}` via {smtp_host}:{smtp_port}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Send an .eml file (with all its attachments) via SMTP without auth"
    )
    parser.add_argument("eml_file", help="Path to the .eml file to send")
    parser.add_argument("smtp_host", help="SMTP server host")
    parser.add_argument(
        "--port", type=int, default=25, dest="smtp_port",
        help="SMTP server port (default: 25)"
    )
    parser.add_argument(
        "--tls", action="store_true", dest="use_tls",
        help="Enable STARTTLS if needed"
    )
    args = parser.parse_args()

    send_eml(
        eml_path=args.eml_file,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        use_tls=args.use_tls
    )
