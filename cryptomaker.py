#! /user/bin/python
#
# cryptomaker.py -- convert text to cryptogram
#
# usage:
#   cryptomaker.py [words to scramble ...]
#
# 

import sys

# print the arguments that were passed in via CLI
arg_index = 0
for arg in sys.argv:
    print("arg[{}] = '{}'".format(arg_index, arg))
    arg_index += 1
