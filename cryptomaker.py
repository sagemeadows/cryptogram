#! /user/bin/python
#
# cryptomaker.py -- convert text to cryptogram
#
# usage:
#   cryptomaker.py [words to scramble ...]
#
#

import sys
import random
import numpy as np

# print the arguments that were passed in via CLI
arg_index = 0
for arg in sys.argv:
    print("arg[{}] = '{}'".format(arg_index, arg))
    arg_index += 1

foo = np.array([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
                ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']])

def shuffle(key_array):
    state = ""
    random.shuffle(key_array[1])
    for i in range(len(key_array[0])):
        if key_array[0][i] != key_array[1][i]:
            state = "good"
        else:
            state = "bad"
            break
    if state == "bad":
        random.shuffle(key_array[1])
        shuffle(key_array)
    else:
        print("Cryptogram code is ready!")

shuffle(foo)
print(foo)
