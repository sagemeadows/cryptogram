**Cryptograms** are word puzzles where each letter of a message is replaced with a different letter of the alphabet. For example:

WKUUP, ZPGUJ! = Hello, World!

Cryptograms are usually fairly long—at least one sentence, often more—so there are enough repetitions of letters to solve the puzzle through trial and error. Some cryptograms offer a hint by telling you what one or two letters map to.

## Create a cryptogram
1. Download `cryptomaker.py`
2. Go to your command line
3. Change directories to wherever you put the downloaded file
4. Run program with `python3 cryptomaker.py [message to encode]`
5. Copy and paste the output to wherever you want it

When you run `cryptomaker.py`, it will return a code, your original message, and the encoded message.

```
$ python3 cryptomaker.py The quick red fox jumps over the lazy brown dog.

Your cryptogram code is:
A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
N  H  X  Q  I  Z  O  G  P  L  U  V  D  T  Y  W  K  S  C  J  A  M  F  E  R  B

Your original message was:
The quick red fox jumps over the lazy brown dog.

Your new message is:
JGI KAPXU SIQ ZYE LADWC YMIS JGI VNBR HSYFT QYO.

Finished!
```

## Solve a cryptogram
1. Download `cryptosolver.py`
2. Go to your command line
3. Change directories to wherever you put the downloaded file
4. Run program...
    - If no letter mappings are known: `python3 cryptomaker.py [cryptogram to decode]`
    - If one letter mapping is known, e.g. A-->B: `python3 cryptomaker.py -c AB [cryptogram to decode]`
    - If two or more letter mappings are known, e.g. A-->B and C-->D: `python3 cryptomaker.py -c AB,CD [cryptogram to decode]`

**WARNING! Cryptograms with many possible solutions will take a long time to complete and may slow down your computer.**

The best cryptograms for this decoder have:
- lots of hints
- 1-letter and/or 2-letter words
    - e.g. *I*, *a*, *it*, *of*, *as*, etc.
- long words with repeating letters
    - e.g. *hopelessness*
- multiple words with overlapping letters
    - e.g. *This sentence is existential and not sentimental*

**WARNING! This decoder cannot handle word-external punctuation.**

Before running `cryptosolver.py`, remove all punctuation except for `'`.
- Good punctuation: `'`
- Bad punctuation: `. , ! ? @ # $ % ^ & * ( ) - _ + = /`

When you run `cryptosolver.py`, it will return the scrambled letters in the message mapped to their unscrambled counterparts. If there are multiple solutions for a letter, it will return _ for that letter.

```
$ python3 cryptosolver.py RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT

A C D E J L Q R T V W X Y
X A H S M C _ T L _ I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL AN_ N_T SENTIMENTAL

This solution took 0.19 seconds.
```

Here is an example with hints provided.

```
$ python3 cryptosolver.py -c QD,VO RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT

A C D E J L Q R T V W X Y
X A H S M C D T L O I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL AND NOT SENTIMENTAL

This solution took 0.19 seconds.
```
