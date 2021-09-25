#! /usr/bin/python
#
# cryptosolver.py
#
# Usage:
#     cryptos.py [word... ]
#
# Given a cryptogram sentence: scans the default "words" file for possible solutions.
#

import collections
import optparse
import sys
import time

def compute_fingerprint(word):
    # Given a 'word': compute a canonical "fingerprint" of the characters within
    # where each character is assigned a letter of the alphabet representing its
    # sequence of "first occurrence".
    #
    # For example: consider the word 'FALLOW'
    #
    # 'F' shows up first and is assigned 'A'
    # 'A' shows up second and is assigned 'B'
    # 'L' shows up third and is assigned 'C'
    # ... and so on D, E, F...
    #
    # Its fingerprint would be 'ABCCDE'
    #
    # The word 'FELLOW' would have the same fingerprint 'ABCCDE'
    # however 'FOLLOW' would be different: 'ABCCBD'
    #
    assignments = {}
    fp = ""
    char_index = 0
    for char in word.upper():
        if (char >= 'A' and char <= 'Z'):
            if char in assignments:
                fp += assignments[char]
            else:
                letter = chr(ord('A') + char_index)
                assignments[char] = letter
                fp += letter
                char_index += 1
        else:
            fp += char
    return fp


def compute_partial_solution(A, B):
    # given two arguments of equal length and same fingerprint:
    # return a partial solution dictionary that would convert A to B
    solution = {}
    for i in range(0, len(A)):
        a = A[i]
        b = B[i]
        if a == b:
            # characters that map to themselves invalidate the solution
            # so we return an empty dictionary
            solution = {}
            break
        solution[a] = b
    return solution


def join_solutions(A, B):
    # given two solutions: A = {a:b, c:d, ...} and B = {...x:y, y:z}
    # join the two dictionaries
    # if there is a conflict: return empty dictionary
    # else: return the join: C = A union B
    C = A.copy()
    items_A = A.items()
    for key_B, value_B in B.items():
        if key_B in A and value_B != A[key_B]:
            # same key but conflicting values
            C = {}
            break
        else:
            solution_is_valid = True
            C[key_B] = value_B
            for key_A, value_A in items_A:
                if value_B == value_A and key_B != key_A:
                    # same value but conflicting keys
                    solution_is_valid = False
                    break
            if not solution_is_valid:
                C = {}
                break
    return C


def apply_solution(solution, A):
    # given a solution and a scrambled word 'A':
    # replace characters in 'A' to produce solved word 'B'
    B = ""
    for i in range(len(A)):
        char = A[i]
        if char in solution:
            B += solution[char]
        else:
            B += char
    return B


def parse_constraint_input(constraint_string):
    # give a constraint string of comma-separated KeyValue characters: "AB,CD,EF"
    # generate a partial solution dictionary: { A:B, C:D, E:F }
    solution = {}
    pairs = constraint_string.upper().split(",")
    known_keys = []
    for pair in pairs:
        if len(pair) == 2:
            key = pair[0]
            value = pair[1]
            if key not in known_keys:
                solution[key] = value
                known_keys.append(key)
    return solution


# parse the options
parser = optparse.OptionParser()
parser.add_option("-c", "--constraint", dest="solution_constraint",
        help="specify a partial solution with comma separated pairs: AB,CD,EF,... (A-->B, C-->D, E-->F, ...)", metavar="AB,CD,EF,...")
(options, args) = parser.parse_args()

# compute the constraint (if any)
constraint = {}
if options.solution_constraint:
    constraint = parse_constraint_input(options.solution_constraint)

# start timer
start = time.time()

# extract the scrambled words from the command-line arguments
scrambled_words = args
## HACK: hard code the input for easy testing
## SENT CENT COST SCENTS SENTIENT SENTENCE
## UAQJ GAQJ GLUJ UGAQJU UAQJVAQJ UAQJAQGA
#scrambled_words = "UAQJ GAQJ GLUJ UGAQJU UAQJVAQJ UAQJAQGA".split()

# build lists of unique:
#   scrambled words
#   fingerprints
#   word lengths (for faster candidate filtering)
unique_scrambled_words = []
fingerprints = []
lengths = []
for word in scrambled_words:
    if word not in unique_scrambled_words:
        unique_scrambled_words.append(word)
        fingerprint = compute_fingerprint(word)
        if fingerprint not in fingerprints:
            fingerprints.append(fingerprint)
        word_length = len(word)
        if word_length not in lengths:
            lengths.append(word_length)

# open the default list of words for reading
words_filename = "/etc/dictionaries-common/words"
try:
    file_handle = open(words_filename, 'r')
except:
    print("failed to open words file '{}'".format(words_filename))
    sys.exit(1)

# create a dictionary:
#   key = fingerprint
#   value = empty array for candidate words
candidates_by_fingerprint = {}
for fingerprint in fingerprints:
    # create an empty array for each fingerprint
    candidates_by_fingerprint[fingerprint] = []


# read each line in words file and sort each candidate word
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
            # only keep words with matching fingerprints
            fingerprint = compute_fingerprint(word)
            if fingerprint in fingerprints:
                # avoid duplicate wordS
                if word not in candidates_by_fingerprint[fingerprint]:
                    candidates_by_fingerprint[fingerprint].append(word)
file_handle.close()

# calculate fingerprints and candidates
candidates_per_scrambled_word = []

for word in unique_scrambled_words:
    fingerprint = compute_fingerprint(word)
    candidates = candidates_by_fingerprint[fingerprint]
    candidates_tuple = (word, fingerprint, len(candidates))
    candidates_per_scrambled_word.append(candidates_tuple)
    ## DEBUG: print the number of candidates for each scrambled word
    #print("DEBUG '{}' has {} candidates".format(word, len(candidates)))
    if len(candidates) == 0:
        print("\nERROR: Could not find solution for {}\n".format(word))
        sys.exit()

## DEBUG: count number of possibilities for each word
## and show time it takes to find possible solutions
#elapsed = round(time.time() - start, 3)
#print("DEBUG 0 t={} len(possible_solutions)={}".format(elapsed, len(final_solutions)))

# sort tuples by number of candidates
candidates_per_scrambled_word = sorted(candidates_per_scrambled_word, key=lambda scrambled_word: scrambled_word[2])
## DEBUG: show sorting worked
#print(candidates_per_scrambled_word)

# create list of sorted unique scrambled words
# and list of sorted fingerprints
sorted_unique_scrambled_words = []
sorted_list_of_fingerprints = []

for i in range(len(candidates_per_scrambled_word)):
    sorted_unique_scrambled_words.append(candidates_per_scrambled_word[i][0])

for i in range(len(candidates_per_scrambled_word)):
    sorted_list_of_fingerprints.append(candidates_per_scrambled_word[i][1])

#
# now that the scrambled words and their fingerprints are sorted
# by number of possible candidates,
# starting with the shortest list of candidates for a word,
# check each candidate for whether it contradicts prior constraints
# and if it doesn't, move on to the candidates for the next word
# and if you reach the end of the lists of candidates,
# print the solution
#

# create starting partial solution and column indices
partial_solution = constraint.copy()
column_indices = [0] * len(sorted_unique_scrambled_words)

column_index = 0

def find_solution(column_index, current_solution):
    ci = column_index
    current_fingerprint = sorted_list_of_fingerprints[ci]
    current_scrambled_word = sorted_unique_scrambled_words[ci]
    for i in range(len(candidates_by_fingerprint[sorted_list_of_fingerprints[ci]])):
        column_indices[ci] = i
        current_candidate = candidates_by_fingerprint[current_fingerprint][i]
        check(current_scrambled_word, current_candidate, current_solution, ci)


def check(current_scrambled_word, current_candidate, current_solution, column_index):
    new_solution = {}
    for i in range(len(current_scrambled_word)):
        new_solution[current_scrambled_word[i]] = current_candidate[i]
    joined_solution = join_solutions(current_solution, new_solution)
    if len(joined_solution) > 0:
        if column_index == len(column_indices) - 1:
            print_solution(joined_solution)
        else:
            find_solution(column_index+1, joined_solution)

print_counter = 0
scrambled_sentence = " ".join(scrambled_words).upper()

def print_solution(solution):
    global print_counter
    print_counter = print_counter + 1
    elapsed = round(time.time() - start, 3)
    print("")
    print("Solution {}, t={}".format(print_counter, elapsed))
    print("")
    sorted_solution = collections.OrderedDict(sorted(solution.items()))
    print(" ".join(sorted_solution.keys()))
    print(" ".join(sorted_solution.values()))
    # print the scrambled input and the solved output
    print("")
    sentence = apply_solution(solution, scrambled_sentence)
    print(" {}".format(scrambled_sentence))
    print(" {}".format(sentence))
    print("")


## end timer
#end = time.time()
#elapsed = end - start
#time_sec = round(elapsed, 2)
#time_min = round((elapsed / 60), 2)

#if elapsed < 60:
    #print("This solution took " + str(time_sec) + " seconds.\n")
#else:
    #print("This solution took " + str(time_min) + " minutes.\n")

find_solution(0, partial_solution)

print("\nAll solutions found!\n")

