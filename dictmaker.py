#!/usr/bin/python

# DictMaker is just an 'spaghetti code' python script that generates different
# types of random passwords, and puts them into a text file altogether.
#
# Usage is dictmaker.py -t <password types> -s <max file size aprox desired>
# Password types are:
#   all         -- Generate all types
#   decent      -- Generate [a-zA-Z0-9]{10} password
#   strong      -- Generate [a-zA-A0-9special]{15} password
#   root        -- Generate [a-zA-Z0-9special]{30} password
#   256_general -- Generate [a-zA-Z0-9]{32} password
#   160_wpa     -- Generate [a-zA-Z0-9special]{20} password
#   504_wpa     -- Generate [a-zA-Z0-9special]{63} password
#   64_wep      -- Generate [A-F0-9]{5} password
#   128_wep     -- Generate [A-F0-9]{13} password
#   152_wep     -- Generate [A-F0-9]{16} password
#   256_wep     -- Generate [A-F0-9]{29} password

# If no flag size is given, bytes is assumed.
# Examples: dictmaker.py -t all -s 50
#           dictmaker.py -t root -s 50B
#           dictmaker.py -t decent -s 50M
#           dictmaker.py -t 256_wep -s 50G
#
# There are probably much better scripts. However, you're free to test this one,
# improve it, share it, or simply ignore it.
# Send your comments to @s0nH4cK or s0nh4ck@gmail.com

import urllib
import sys
import base64
import os.path
import string
import argparse
import random

VERSION = '0.0.1alpha'
# Path and name of the dictionary
# Path must exist!
dictionary = './dictionary.txt'

types_dict = {'decent':'gen_decent_pass()', 'strong':'gen_strong_pass()', 'root':'gen_root_pass()',\
              '256_general':'gen_256_pass()', '160_wpa':'gen_160_wpa_pass()',\
              '504_wpa':'gen_504_wpa_pass()', '64_wep':'gen_64_wep_pass()',\
              '128_wep':'gen_128_wep_pass()', '152_wep':'gen_152_wep_pass()',\
              '256_wep':'gen_256_wep_pass()'}

def banner():
    print "________  .__        __     _____          __                 \n" + \
          "\______ \ |__| _____/  |_  /     \ _____  |  | __ ___________ \n" + \
          " |    |  \|  |/ ___\   __\/  \ /  \\\__  \ |  |/ // __ \_  __ \ \n" + \
          " |    `   \  \  \___|  | /    Y    \/ __ \|    <\\  ___/|  | \/\n" + \
          "/_______  /__|\___  >__| \____|__  (____  /__|_ \\\___  >__|   \n" + \
          "        \/        \/             \/     \/     \/    \/       \n" + \
          "" + VERSION + "                                      by @s0nH4cK\n" + \
          "                                                "

def convert_size(max_size_input):
    max_size = 0
    if max_size_input[-1] == 'B':
        max_size = int(max_size_input[:-1])
    elif max_size_input[-1] == 'K':
        max_size = int(max_size_input[:-1]) * 1024
    elif max_size_input[-1] == 'M':
        max_size = int(max_size_input[:-1]) * 1024**2
    elif max_size_input[-1] == 'G':
        max_size = int(max_size_input[:-1]) * 1024**3
    else:
        max_size = int(max_size_input)
        
    return max_size

def gen_decent_pass():
    word = ''
    for i in range(10):
        word += random.choice(string.lowercase + string.uppercase + string.digits)
    return word
def gen_strong_pass():
    word = ''
    for i in range(15):
        word += random.choice(string.lowercase + string.uppercase + string.digits + string.punctuation)
    return word
def gen_root_pass():
    word = ''
    for i in range(30):
        word += random.choice(string.lowercase + string.uppercase + string.digits + string.punctuation)
    return word
def gen_256_pass():
    word = ''
    for i in range(32):
        word += random.choice(string.lowercase + string.uppercase + string.digits)
    return word
def gen_160_wpa_pass():
    word = ''
    for i in range(20):
        word += random.choice(string.lowercase + string.uppercase + string.digits + string.punctuation)
    return word
def gen_504_wpa_pass():
    word = ''
    for i in range(63):
        word += random.choice(string.lowercase + string.uppercase + string.digits + string.punctuation)
    return word
def gen_64_wep_pass():
    word = ''
    for i in range(5):
        word += random.choice('ABCDEF' + string.digits)
    return word
def gen_128_wep_pass():
    word = ''
    for i in range(13):
        word += random.choice('ABCDEF' + string.digits)
    return word
def gen_152_wep_pass():
    word = ''
    for i in range(16):
        word += random.choice('ABCDEF' + string.digits)
    return word
def gen_256_wep_pass():
    word = ''
    for i in range(29):
        word += random.choice('ABCDEF' + string.digits)
    return word

def get_dict_size(dictionary):
    dict_size = os.path.getsize(dictionary)
    dict_size_str = ''
    if dict_size / 1024 > 0:
        dict_size_str = str(round(float(dict_size) / float(1024), 2)) + 'K'
        if dict_size / 1024**2 > 0:
            dict_size_str = str(round(float(dict_size) / float(1024**2), 2)) + 'M'
            if dict_size / 1024**3 > 0:
                dict_size_str = str(round(float(dict_size) / float(1024**3), 2)) + 'G'
    return dict_size_str

if __name__ == '__main__':    
    banner()
    
    parser = argparse.ArgumentParser(description='DictMaker is just an "spaghetti code" \
    python script that generates different types of random passwords, and puts them into \
    a text file altogether.')
    parser.add_argument('-t', '--type', type=str, nargs='+', help='Type of passwords to be generated', required = True)
    parser.add_argument('-s', '--size', type=str, help='Size of dictionary to be generated', required = True)
    args = parser.parse_args()
    
    types = args.type
    max_size = convert_size(args.size)
    
    if not os.path.exists(dictionary):
        os.system('touch ' + dictionary)
    
    dict_size = int(os.path.getsize(dictionary))
    print '[+] Generating passwords...'
    while dict_size < max_size:
        f = open(dictionary, 'a')
        all = False
        for type in types:
            if type == 'all':
                all = True
                break
        password = ''
        if all:
            for type in types_dict:
                password = eval(types_dict[type])
                f.write(password + '\n')
        else:
            for type in types:
                password = eval(types_dict[type])
                f.write(password + '\n')
                
        f.flush()    
        f.close()
        dict_size = int(os.path.getsize(dictionary))
        
    dict_size_str = get_dict_size(dictionary)
    print '[++] Total file size generated: ' + dict_size_str
    print '[+] Dictionary finished successfully\n'
