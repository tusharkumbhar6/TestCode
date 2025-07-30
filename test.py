#!/usr/bin/env python3
import argparse
import smtplib
from email import policy
from email.parser import BytesParser

def send_eml(eml_path, smtp_host, smtp_port=25, use_tls=False):
    # 1) Parse the raw .eml
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.SMTP).parse(f)

    # 2) Determine envelope sender
    envelope_from = msg.get('Return-Path')
    if not envelope_from:
        envelope_from = msg.get('From')

    # 3) Gather envelope recipients
    recipients = []
    for hdr in ('To', 'Cc', 'Bcc'):
        vals = msg.get_all(hdr, [])
        # msg.get_all returns list of header‑value strings; split commas
        for v in vals:
            recipients += [addr.strip() for addr in v.split(',') if addr.strip()]

    # 4) Remove Bcc header so it doesn't appear in the message
    if 'Bcc' in msg:
        del msg['Bcc']

    # 5) Connect & send
    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.set_debuglevel(1)   # comment out or set to 0 to silence
        if use_tls:
            smtp.starttls()
        # send_message will use msg.as_bytes() under the hood
        smtp.send_message(msg,
                          from_addr=envelope_from,
                          to_addrs=recipients)
        print(f"Sent {eml_path} from {envelope_from} to {recipients}")

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Relay a .eml file exactly as‑is via SMTP (no auth)"
    )
    p.add_argument('eml_file', help='Path to the .eml file')
    p.add_argument('smtp_host', help='SMTP server host')
    p.add_argument('--port', type=int, default=25, dest='smtp_port',
                   help='SMTP port (default: 25)')
    p.add_argument('--tls', action='store_true', dest='use_tls',
                   help='Use STARTTLS before sending')
    args = p.parse_args()

    send_eml(args.eml_file, args.smtp_host, args.smtp_port, args.use_tls)
