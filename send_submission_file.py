#!/usr/bin/env python3
import argparse
import sys
sys.path.append("/root/bin")
from mail_handler import *
parser = argparse.ArgumentParser(prog='cmiyc submission')
parser.add_argument('--file', help='use this option give the file path of the file to encrypt')
parser.add_argument('--to', help='use this option give the file path of the file to encrypt')
parser.add_argument('--subject', help='use this option to give the email a subject')
args = parser.parse_args()
if args.file and args.to and args.subject:
    with open(args.file, "r") as f:
        body = f.read()
    sent_status = send_encrypted_email(
        args.subject,
        body,
        "cmiyc2022@denard.me",
        args.to
    )
    print(f"sent status: {sent_status}")
else:
    print("you forgot some args")