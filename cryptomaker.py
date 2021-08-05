#! /user/bin/python
#
# cryptomaker.py -- convert text to cryptogram
#
# usage:
#   cryptomaker.py [words to scramble ...]
#
#

import sys
import string
import random
import numpy as np

#cryptogram pre-key
foo = np.array([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
                ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']])

#create cryptogram key
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
        print("\nYour cryptogram code is:")
        key = "  ".join(foo[0])
        value = "  ".join(foo[1])
        print(key)
        print(value)

#prepare message
def arrange(message):
    message.remove("cryptomaker.py")
    message = " ".join(message)
    swap(message)

#encode message
def swap(message):
    print("\nYour original message was:\n" + message)
    key = "abcdefghijklmnopqrstuvwxyz"
    value = "".join(foo[1])
    message = message.lower()
    for c in message:
        for i in range(len(key)):
            if c.upper() == foo[0][i]:
                message = message.replace(c, value[i])
                break
    print("\nYour new message is:\n" + message)
    print("\nFinished!")

#run program
shuffle(foo)
arrange(sys.argv)
