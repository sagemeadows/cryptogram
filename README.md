**Cryptograms** are word puzzles where each letter of a message is replaced with a different letter of the alphabet. For example:

WKUUP, ZPGUJ! = Hello, World!

Cryptograms are usually fairly long—at least one sentence, often more—so there are enough repetitions of letters to solve the puzzle through trial and error. Some cryptograms offer a hint by telling you what one or two letters map to.

## Create a cryptogram
1. Download `cryptomaker.py`
2. Go to your command line
3. Change directories to wherever you put the downloaded file
4. Run script with `python3 cryptomaker.py [message to encode]`
5. Copy and paste the output to wherever you want it

**WARNING!**
\
`cryptomaker.py` does not preserve apostrophes or quotation marks, and does not work at all if there is an odd number of apostrophes and quotation marks in the message. Remove `'` and `"` prior to running script.

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
4. Run script...
    - If no letter mappings are known: `python3 cryptomaker.py [cryptogram to decode]`
    - If one letter mapping is known, e.g. A-->B: `python3 cryptomaker.py -c AB [cryptogram to decode]`
    - If two or more letter mappings are known, e.g. A-->B and C-->D: `python3 cryptomaker.py -c AB,CD,... [cryptogram to decode]`

**WARNING! Cryptograms with very many possible solutions will take a long time to complete and may slow down your computer.**
\
The best cryptograms for this decoder have:
- lots of hints
- 1-letter and/or 2-letter words
    - e.g. *I*, *a*, *it*, *of*, *as*, etc.
- long words
    - e.g. *independence*
- multiple words with overlapping letters
    - e.g. *This sentence is existential and not sentimental*

**WARNING! This decoder cannot handle word-external punctuation.**
\
Before running `cryptosolver.py`, remove all punctuation.

When you run `cryptosolver.py`, it will return every possible solution with the scrambled letters in the message mapped to their unscrambled counterparts.

```
$ python3 cryptosolver.py RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT

Solution 1, t=0.179

A C D E J L Q R T V W X Y
X A H S M C D T L O I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL AND NOT SENTIMENTAL


Solution 2, t=0.182

A C D E J L Q R T V W X Y
X A H S M C D T L U I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL AND NUT SENTIMENTAL


Solution 3, t=0.186

A C D E J L Q R T V W X Y
X A H S M C Y T L O I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL ANY NOT SENTIMENTAL


Solution 4, t=0.189

A C D E J L Q R T V W X Y
X A H S M C Y T L U I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL ANY NUT SENTIMENTAL


All solutions found!
```

Here is an example with hints provided.

```
$ python3 cryptosolver.py -c QD,VO RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT

Solution 1, t=0.18

A C D E J L Q R T V W X Y
X A H S M C D T L O I E N

 RDWE EXYRXYLX WE XAWERXYRWCT CYQ YVR EXYRWJXYRCT
 THIS SENTENCE IS EXISTENTIAL AND NOT SENTIMENTAL


All solutions found!
```
