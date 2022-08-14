#!/usr/bin/env python3
import argparse
import sys
sys.path.append("/root/bin")
from mail_handler import *
parser = argparse.ArgumentParser(prog='cmiyc decrypt file')
parser.add_argument('--file', help='use this option give the file path of the file to encrypt')
args = parser.parse_args()
if args.file:
    decrypt_file_path = f"{args.file}.txt"
    gpg_decrypt_file(args.file, decrypt_file_path)
    with open(decrypt_file_path, "r") as f:
        print(f.read())
else:
    print("you forgot some args")