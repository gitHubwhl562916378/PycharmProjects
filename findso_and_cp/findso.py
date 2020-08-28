#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-

import subprocess
import re
import os
import argparse

parser = argparse.ArgumentParser(prog='find_so')
parser.add_argument('--so_db_dir', default='so', type=str, help='copy all valid so dir')
parser.add_argument('--so_dest_dir', default='so', type=str, help='copy needed so to dest dir')
parser.add_argument('--copy_2_dest', action='store_true', default=False, help='copy file to text, or copy so to dest_dir')
parser.add_argument('--source_file', type=str, default=None, help='binary or *.so')
args = parser.parse_args()

so_db_dir = args.so_db_dir
so_dest_dir = args.so_dest_dir
copy_2_dest = args.copy_2_dest
so_or_exectuable_path = args.source_file

def copy_all_so_2_db():
    if not os.path.exists(so_db_dir):
        os.mkdir(so_db_dir)

    fh = subprocess.Popen("ldd -r " + so_or_exectuable_path, stdout=subprocess.PIPE, shell=True)
    arr = fh.stdout.readlines()
    patten = re.compile(r'.+ => (.+) \(')

    for line in arr:
        content = line.decode('ascii')
        content = content.replace('\t', '')
        res = patten.match(content)
        if res:
            so_name_path = res.group(1)
            
            if os.path.islink(so_name_path):
                target_file = os.path.realpath(so_name_path)

                print('copy {} => {}'.format(target_file, so_db_dir))
                os.system('cp ' + target_file + ' ' + so_db_dir)
                print('copy link {} => {}'.format(so_name_path, so_db_dir))
                os.system('cp -d ' + so_name_path + ' ' + so_db_dir)
            else:
                print('copy {} => {}'.format(so_name_path, so_db_dir))
                os.system('cp ' + so_name_path + ' ' + so_db_dir)

def copy_need_2_dest():
    if not os.path.exists(so_dest_dir):
        os.mkdir(so_dest_dir)
    while True:
        fh = subprocess.Popen("ldd -r " + so_or_exectuable_path, stdout=subprocess.PIPE, shell=True)
        arr = fh.stdout.readlines()
        patten = re.compile(r'(.+) => not found')

        hand_len = 0
        for line in arr:
            content = line.decode('ascii')
            content = content.replace('\t', '')
            res = patten.match(content)
            if res:
                so_name = res.group(1)
                existed_so_name_path = so_db_dir + "/" + so_name
                if os.path.islink(existed_so_name_path):
                    target_file = os.path.realpath(existed_so_name_path)

                    print('copy {} => {}'.format(target_file, so_dest_dir))
                    os.system('cp ' + target_file + ' ' + so_dest_dir)
                    print('copy link {} => {}'.format(existed_so_name_path, so_dest_dir))
                    os.system('cp -d ' + existed_so_name_path + ' ' + so_dest_dir)
                else:
                    print('copy {} => {}'.format(existed_so_name_path, so_dest_dir))
                    os.system('cp ' + existed_so_name_path + ' ' + so_dest_dir)
                
                hand_len = hand_len + 1
        
        if not hand_len:
            break
    
if __name__ == "__main__":
    if copy_2_dest:
        copy_need_2_dest()
    else:
        copy_all_so_2_db()