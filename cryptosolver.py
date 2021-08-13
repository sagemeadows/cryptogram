#! /usr/bin/python
#
# cryptosolver.py
#
# Usage:
#     cryptos.py [word... ]
#
# Given a cryptogram sentence: scans the default "words" file for possible solutions.
#

#import argparse
import collections
import sys

def compute_fingerprint(word):
    # Given a 'word': compute a canonical "fingerprint" of the characters within
    # where each character is assigned a letter of the alphabet representing its sequence
    # of "first occurrence".
    #
    # For example: consider the word 'fallow'
    #
    # f shows up first and is assigned A
    # a shows up second and is assigned B
    # l shows up third and is assigned C
    # ... and so on
    #
    # Its fingerprint would be 'ABCCDE'
    #
    # The word 'fellow' would have the same fingerprint 'ABCCDE'
    # however 'follow' would be different: 'ABCCBD'
    # 
    char_map = {}
    fingerprint = ""
    i = 0
    WORD = word.upper()
    for char in WORD:
        if (char >= 'A' and char <= 'Z'):
            if char in char_map:
                fingerprint += char_map[char]
            else:
                letter = chr(ord('A') + i)
                char_map[char] = letter
                fingerprint += letter
                i += 1
        else:
            fingerprint += char
    return fingerprint


def compute_partial_solution(scrambled_word, word):
    # given two arguments of equal length and same fingerprint:
    # return a partial solution dictionary that would convert scrambled_word to word
    solution = {}
    for i in range(0, len(scrambled_word)):
        a = scrambled_word[i]
        b = word[i]
        if a == b:
            # characters that map to themselves invalidate the solution
            # so we return an empty dictionary
            solution = {}
            break
        solution[a] = b
    return solution


def join_solutions(solution_A, solution_B):
    # given two mappings: {a:b, c:d, ...} and {...x:y, y:z} join the two maps
    # if there is a conflict: return empty dictionary
    # else: return the join
    combined_solution = solution_A
    items_A = solution_A.items()
    for key_B, value_B in solution_B.items():
        if key_B in solution_A and value_B != solution_A[key_B]:
            # conflicting mapping
            combined_solution = {}
            break;
        else:
            solution_is_valid = True
            combined_solution[key_B] = value_B
            for key_A, value_A in items_A:
                if value_B == value_A and key_B != key_A:
                    # double-mapping
                    solution_is_valid = False
                    break;
            if not solution_is_valid:
                combined_solution = {}
                break;
    return combined_solution


def apply_solution(solution, scramble):
    # given a solution (dictionary of (char --> char) pairs):
    # replace characters in 'scramble' to produce the 'word'
    word = ""
    for i in range(len(scramble)):
        if scramble[i] in solution:
            word += solution[scramble[i]]
        else:
            word += scramble[i]
    return word

    

# extract the scrambled words from the command-line arguments
scrambled_words = sys.argv[1:]

# build a list of unique scrambled words (eliminate duplicates)
# and also a list of unique: fingerprints
# and lengths (for faster candidate filtering)
fingerprints = []
lengths = []
unique_scrambled_words = []
for word in scrambled_words:
    WORD = word.upper()
    if WORD not in unique_scrambled_words:
        unique_scrambled_words.append(WORD)
        fingerprint = compute_fingerprint(word)
        if fingerprint not in fingerprints:
            fingerprints.append(fingerprint)
        word_length = len(word)
        if word_length not in lengths:
            lengths.append(word_length)

# open the default list of words for reading
WORDS = "/etc/dictionaries-common/words"
try:
    file_handle = open(WORDS, 'r')
except:
    print("failed to open WORDS file '{}'".format(WORDS))
    sys.exit(1)

# create a dictionary:
#   key = fingerrpint
#   value = empty array for candidates
candidates_by_fingerprint = {}
for fingerprint in fingerprints:
    # create an empty array for each fingerprint
    candidates_by_fingerprint[fingerprint] = []

# read each line in WORDS file and sort each candidate
# by fingerprint into its respective array
num_lines = 0
while True:
    num_lines += 1
    line = file_handle.readline().upper()
    if not line:
        # at end of file
        break
    # split the line just in case a it has multiple words
    words = line.split()
    for word in words:
        # skip words whose lengths don't match
        if len(word) in lengths:
            # skip words whose fingerprints don't match
            fingerprint = compute_fingerprint(word)
            if fingerprint in fingerprints:
                # avoid duplicate entries in the array
                if word not in candidates_by_fingerprint[fingerprint]:
                    candidates_by_fingerprint[fingerprint].append(word)
file_handle.close()


# for each (word, candidate) pair: generate the partial solution
# which is a dictionary of (key,value) pairs (char --> char)
solutions = {}
for word in unique_scrambled_words:
    # insert an empty list into the dictionary
    solutions[word] = []
    fingerprint = compute_fingerprint(word)
    candidates = candidates_by_fingerprint[fingerprint]
    for candidate in candidates:
        solution = compute_partial_solution(word, candidate)
        if len(solution) > 0:
            # only non-empty solutions are allowed
            solutions[word].append(solution)

# now that we all possible partial solutions...
# join each one to all the others and discard conflicts
# (e.g. solutions which try to map same key to different value or visa-versa)
i = 0
final_solutions = solutions[unique_scrambled_words[i]]
for i in range(1, len(unique_scrambled_words)):
    key = unique_scrambled_words[i]
    new_solutions = []
    for solution in solutions[key]:
        for joined_solution in final_solutions:
            new_solution = join_solutions(solution, joined_solution)
            if len(new_solution) > 0:
                new_solutions.append(new_solution)
    final_solutions = new_solutions

# time to print the results
scrambled_sentence = " ".join(scrambled_words).upper()
for solution in final_solutions:
    # sort the solution's keys alphabetically
    sorted_solution = collections.OrderedDict(sorted(solution.items()))

    # print the solution in two lines
    print(" ".join(sorted_solution.keys()))
    print(" ".join(sorted_solution.values()))

    # print the scrambled intput and the solved output in two lines
    sentence = apply_solution(solution, scrambled_sentence)
    print("  {}".format(scrambled_sentence))
    print("  {}\n".format(sentence))


