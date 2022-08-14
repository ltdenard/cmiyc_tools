#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser(prog='cmiyc sort and remove previous')
parser.add_argument('--last', help='use this option give the file path of last submissions')
parser.add_argument('--new', help='use this option give the file path of new submission')
parser.add_argument('--sfile', help='use this option to give the submit file name')
args = parser.parse_args()

with open(args.last, 'r') as f:
    last_list = f.read().splitlines()

with open(args.new, 'r') as f:
    new_list = f.read().splitlines()

diff_list = list(set(new_list)-set(last_list))
with open(args.sfile, 'w') as f:
    f.write('\n'.join(diff_list).strip())
    f.write('\n')