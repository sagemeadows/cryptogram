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

#cryptogram pre-key
code = {"key": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        "value": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', \
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']}

#create cryptogram key
def shuffle(key_dict):
    state = ""
    new_list = []
    random.shuffle(key_dict["value"])
    for i in range(len(key_dict["key"])):
        key = key_dict["key"][i]
        value = key_dict["value"][i]
        this_tuple = (key, value)
        new_list.append(this_tuple)
    # DEBUG: show new_list
    #print("\n" + str(new_list))
    for x in new_list:
        # DEBUG: print tuples
        #print(x)
        if x[0] == x[1]:
            state = "bad"
            # DEBUG: show bad run
            #print(" BAD RUN")
            #print("")
            # end debug
            break
    if state == "bad":
        shuffle(key_dict)
    else:
        print("\nYour cryptogram code is:")
        key = "  ".join(key_dict["key"])
        value = "  ".join(key_dict["value"])
        print(key)
        print(value)


#encode message
def swap(message):
    message = " ".join(message[1:])
    print("\nYour original message was:\n" + message)
    key = "abcdefghijklmnopqrstuvwxyz"
    value = "".join(code["value"])
    message = message.lower()
    for c in message:
        for i in range(len(key)):
            if c.upper() == code["key"][i]:
                message = message.replace(c, value[i])
                break
    print("\nYour new message is:\n" + message)
    print("\nFinished!\n")

#run script
shuffle(code)
swap(sys.argv)
