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
`cryptomaker.py` does not automatically preserve apostrophes or quotation marks inside the message to be encoded. If you want an apostrophe or quotation mark in the message, put a backslash `\` before `'` or `"`.

When you run `cryptomaker.py`, it will return a code, your original message, and the encoded message.

```
$ python3 cryptomaker.py My best friend\'s other friend\'s cousin\'s teacher\'s substitute said, \"Don\'t make your sentences too confusing.\"

Your cryptogram code is:
A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
Y  C  Z  J  F  P  I  U  N  Q  X  W  H  S  M  T  L  A  D  O  G  K  B  R  V  E

Your original message was:
My best friend's other friend's cousin's teacher's substitute said, "Don't make your sentences too confusing!"

Your new message is:
HV CFDO PANFSJ'D MOUFA PANFSJ'D ZMGDNS'D OFYZUFA'D DGCDONOGOF DYNJ, "JMS'O HYXF VMGA DFSOFSZFD OMM ZMSPGDNSI!"

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

**WARNING! Be careful of punctuation in cryptograms.**
\
Some punctuation symbols need to have a backslash `\` before them in order for the script to work. Put `\` before any of the following characters:
```
' " ` ; ! & < > ( ) |
```

When you run `cryptosolver.py`, it will return every possible solution with the scrambled letters in the message mapped to their unscrambled counterparts.

```
$ python3 cryptosolver.py CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV

Solution 1, t=2.046

A C E G H K O Q S U V X Z
C T S N G O A R E I Y H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SCENT THEIR MONEY


Solution 2, t=2.164

A C E G H K O Q S U V X Z
L T S P G O A R E I D H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SLEPT THEIR MOPED


Solution 3, t=2.445

A C E G H K O Q S U V X Z
P T S N G O A R E I Y H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SPENT THEIR MONEY


Solution 4, t=2.577

A C E G H K O Q S U V X Z
W T S P G O A R E I D H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SWEPT THEIR MOPED

All solutions found!
```

Here is an example with hints provided.

```
$ python3 cryptosolver.py CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV -c CT,XH,ES

Solution 1, t=0.119

A C E G H K O Q S U V X Z
C T S N G O A R E I Y H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SCENT THEIR MONEY


Solution 2, t=0.132

A C E G H K O Q S U V X Z
L T S P G O A R E I D H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SLEPT THEIR MOPED


Solution 3, t=0.158

A C E G H K O Q S U V X Z
P T S N G O A R E I Y H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SPENT THEIR MONEY


Solution 4, t=0.194

A C E G H K O Q S U V X Z
W T S P G O A R E I D H M

  CXS CXQSS OZUHKE EASGC CXSUQ ZKGSV
  THE THREE AMIGOS SWEPT THEIR MOPED

All solutions found!
```

Providing a constraint makes the solver significantly faster.

Here's an example with punctuation symbols:

```
$ python3 cryptosolver.py HV CFDO PANFSJ\'D MOUFA PANFSJ\'D ZMGDNS\'D OFYZUFA\'D DGCDONOGOF DYNJ, \"JMS\'O HYXF VMGA DFSOFSZFD OMM ZMSPGDNSI\!\" -c HM,VY,XK

Solution 1, t=0.293

A C D F G H I J M N O P S U V X Y Z
R B S E U M G D O I T F N H Y K A C

  HV CFDO PANFSJ'D MOUFA PANFSJ'D ZMGDNS'D OFYZUFA'D DGCDONOGOF DYNJ, "JMS'O HYXF VMGA DFSOFSZFD OMM ZMSPGDNSI!"
  MY BEST FRIEND'S OTHER FRIEND'S COUSIN'S TEACHER'S SUBSTITUTE SAID, "DON'T MAKE YOUR SENTENCES TOO CONFUSING!"

All solutions found!
```
