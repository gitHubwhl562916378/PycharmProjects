#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

import subprocess
import re
import os
import argparse

parser = argparse.ArgumentParser(prog='find_so')
parser.add_argument('--dest_dir', default='so', type=str, help='copy so to dest dir')
parser.add_argument('--find_so_2_file', action='store_true', default=False, help='copy file to text, or copy so to dest_dir')
parser.add_argument('--source_file', type=str, default=None, help='binary or *.so')
parser.add_argument('--output_file', default='output', type=str, help='copy file so need to output_file')
args = parser.parse_args()

dest_dir = args.dest_dir
so_or_exectuable_path = args.source_file
is_to_file = args.find_so_2_file
out_file = None
file_mode = ""

if not is_to_file:
    file_mode = "r"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print('mkdir %s'%(dest_dir))
else:
    file_mode = "w"

out_file = open(args.output_file, file_mode)
fh = subprocess.Popen("ldd -r " + so_or_exectuable_path, stdout=subprocess.PIPE, shell=True)
arr = fh.stdout.readlines()

patten = None
so_not_find = []
if is_to_file:
    patten = re.compile(r'(.+) => not found')
else:
    iter_f = iter(out_file)
    so_not_find = [so.split('\n')[0] for so in iter_f]
    
    patten = re.compile(r'(.+) => (.+) \(')

for line in arr:
    content = line.decode('ascii')
    content = content.replace('\t', '')
    res = patten.match(content)
    if res:
        if is_to_file:
            print(res.group())
            out_file.write(res.group(1) + "\n")
        else:
            so_name = res.group(1)
            so_name_path = res.group(2)
            if not so_not_find.count(so_name):
                continue
            
            if os.path.islink(so_name_path):
                target_file = os.path.realpath(so_name_path)

                print('copy {} => {}'.format(target_file, dest_dir))
                os.system('cp ' + target_file + ' ' + dest_dir)
                print('copy link {} => {}'.format(so_name_path, dest_dir))
                os.system('cp -d ' + so_name_path + ' ' + dest_dir)
            else:
                print('copy {} => {}'.format(so_name_path, dest_dir))
                os.system('cp ' + so_name_path + ' ' + dest_dir)
