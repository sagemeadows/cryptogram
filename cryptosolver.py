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
import string

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

def parse_known_values(constraint_string):
    # give a constraint string of comma-separated KeyValue characters: "AB,CD,EF"
    # generate a list of known values: [ B, D, F ]
    pairs = constraint_string.upper().split(",")
    known_values = []
    for pair in pairs:
        if len(pair) == 2:
            key = pair[0]
            value = pair[1]
            if value not in known_values:
                known_values.append(value)
    return known_values

def compute_fingerprint(word):
    # Given a 'word': compute a canonical "fingerprint" of the characters within
    # where each unknown character is assigned a lowercase letter of the alphabet 
    # representing its sequence of "first occurrence", and
    # each known character is assigned its value in uppercase.
    #
    # For example: consider the word 'FALLOW'
    #
    # 'F' shows up first and is assigned 'a'
    # 'A' shows up second and is assigned 'b'
    # 'L' shows up third and is assigned 'c'
    # ... and so on D, E, F...
    #
    # Its fingerprint would be 'abccde'
    #
    # The word 'FELLOW' would have the same fingerprint 'abccde'
    # however 'FOLLOW' would be different: 'abccbd'
    #
    # For a scrambled word BPKKYU if we knew that K:A,
    # its fingerprint would be 'abLLcd'
    #
    assignments = constraint.copy()
    fp = ""
    char_index = 0
    for char in word.upper():
        if (char >= 'A' and char <= 'Z'):
            if char in assignments:
                fp += assignments[char]
            else:
                letter = chr(ord('a') + char_index)
                assignments[char] = letter
                fp += letter
                char_index += 1
        else:
            fp += char
    return fp

def compute_candidate_fingerprint(word):
    # Given a word: compute a canonical "fingerprint" of the characters within
    # where each unknown character is assigned a lowercase letter of the alphabet 
    # representing its sequence of "first occurrence", and
    # each known character is assigned its own value in uppercase.
    #
    #known_values = known_values
    assignments = {}
    fp = ""
    char_index = 0
    for char in word.upper():
        if (char >= 'A' and char <= 'Z'):
            if char in assignments:
                fp += assignments[char]
            else:
                if char in known_values:
                    assignments[char] = char
                    fp += char
                else:
                    letter = chr(ord('a') + char_index)
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
        if a != chr(39):
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


# parse the options
parser = optparse.OptionParser()
parser.add_option("-c", "--constraint", dest="solution_constraint",
        help="specify a partial solution with comma separated pairs: AB,CD,EF,... (A-->B, C-->D, E-->F, ...)", metavar="AB,CD,EF,...")
(options, args) = parser.parse_args()

# compute the constraint (if any)
constraint = {}
known_values = []
if options.solution_constraint:
    constraint = parse_constraint_input(options.solution_constraint)
    known_values = parse_known_values(options.solution_constraint)
    ## DEBUG
    #print("DEBUG: The known values are " + str(known_values))

# start timer
start = time.time()

# extract the scrambled words from the command-line arguments
scrambled_input = args
scrambled_words = scrambled_input.copy()
safe_characters = []
safe_characters.append(chr(39))
for char in string.ascii_uppercase:
    safe_characters.append(char)
for char in string.ascii_lowercase:
    safe_characters.append(char)

for i in range(len(scrambled_words)):
    for char in scrambled_words[i]:
        if char not in safe_characters:
            scrambled_words[i] = scrambled_words[i].replace(char, "")
## DEBUG: show removal of word-external punctuation
#print(scrambled_words)

## DEBUG HACK: hard code the input for easy testing
#print("SENT CENT COST SCENTS SENTIENT SENTENCE")
#print("UAQJ GAQJ GLUJ UGAQJU UAQJVAQJ UAQJAQGA")
#scrambled_words = "UAQJ GAQJ GLUJ UGAQJU UAQJVAQJ UAQJAQGA".split()

# bail if we have no input
if len(scrambled_words) == 0:
    # TODO: print usage info here
    sys.exit(0)

solution_counter = 0
scrambled_sentence = " ".join(scrambled_input).upper()
## DEBUG
#print(scrambled_sentence + "\n")

def print_solution(solution):
    global solution_counter
    global scrambled_sentence;
    solution_counter = solution_counter + 1
    elapsed = round(time.time() - start, 3)
    print("")
    print("Solution {}, t={}".format(solution_counter, elapsed))
    print("")
    sorted_solution = collections.OrderedDict(sorted(solution.items()))
    print(" ".join(sorted_solution.keys()))
    print(" ".join(sorted_solution.values()))
    # print the scrambled input and the solved output
    print("")
    sentence = apply_solution(solution, scrambled_sentence)
    print(" ", scrambled_sentence)
    print(" ", sentence)
    print("")

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
            fingerprint = compute_candidate_fingerprint(word)
            if fingerprint in fingerprints:
                # avoid duplicate wordS
                if word not in candidates_by_fingerprint[fingerprint]:
                    candidates_by_fingerprint[fingerprint].append(word)
file_handle.close()

# sort scrambled_words by number of candidates
# by building tuples: [scrambled_word, number_of_candidates]
# and sorting by second field
sortable_tuples = []
for word in unique_scrambled_words:
    fingerprint = compute_fingerprint(word)
    candidates = candidates_by_fingerprint[fingerprint]
    this_tuple = (word, candidates)
    sortable_tuples.append(this_tuple)
    ## DEBUG: print the number of candidates for each scrambled word
    #print("DEBUG '{}' has {} candidates that match '{}'".format(word, len(candidates), fingerprint))
    if len(candidates) == 0:
        print("\nERROR: Could not find solution for {}\n".format(word))
        sys.exit()
sorted_tuples = sorted(sortable_tuples, key=lambda entry: len(entry[1]))

## DEBUG: show sorting worked
#for t in sorted_tuples:
#    print("word={} num_candidates={}".format(t[0], len(t[1])))

# now that the tuples are sorted by number of possible candidates,
# we will hunt for viable solutions column by column:
# We'll start with the first column and check candidates until we find one
# that does not violate our constraint.  From there we'll move to the top
# of the next column and do the same thing, building a more complete partial
# solution as we add compatible words and moving to subsequent columns.
# When we find a valid word in ALL columns we'll print the solution and
# continue walking the last column.
# When we reach the end of any column we'll back up to the previous column
# and pick up where we left off.

# create starting partial solution and column indices
num_columns = len(sorted_tuples)
candidate_indices = [0] * num_columns # where we are in each column of candidates
partial_solutions = [{}] * num_columns # partial solutions at the start of each column
partial_solutions[0] = constraint
column_index = 0

while True:
    scrambled_word = sorted_tuples[column_index][0]
    candidates = sorted_tuples[column_index][1]
    candidate_index = candidate_indices[column_index]
    num_candidates = len(candidates)
    partial_solution = partial_solutions[column_index]
    while candidate_index < num_candidates:
        word = candidates[candidate_index]
        candidate_solution = compute_partial_solution(scrambled_word, word)
        if len(candidate_solution) > 0:
            joined_solution = join_solutions(partial_solution, candidate_solution)
            if len(joined_solution) > 0:
                # we've found a non-conflicting word
                if column_index == num_columns - 1:
                    # we're walking the last column and our solution is complete
                    print_solution(joined_solution)
                else:
                    # remember our place and proceed to the next column of candidates
                    candidate_indices[column_index] = candidate_index
                    column_index += 1
                    partial_solutions[column_index] = joined_solution
                    candidate_indices[column_index] = 0
                    break
        candidate_index += 1

    if candidate_index == num_candidates:
        # we've reached the end of this column so we back up
        # to the previous and pick up where we left off
        column_index -= 1
        if column_index < 0:
            # we've searched everything
            break;
        candidate_indices[column_index] += 1

print("All solutions found!\n")

