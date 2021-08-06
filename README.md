**Cryptograms** are word puzzles where each letter of a message is replaced with a different letter of the alphabet. For example:

WKUUP, ZPGUJ! = Hello, World!

Cryptograms are usually at least a sentence long, so there are enough repetitions of letters to solve the puzzle through trial and error. Some cryptograms offer a hint by telling you what one or two letters map to.

## Create a cryptogram
1. Download `cryptomaker.py`
2. Go to your command line
3. Change directories to wherever you put the downloaded file
4. Invoke the file with `python cryptomaker.py`, followed by the message you want to encode
5. Copy and paste the output to wherever you want it

When you run `cryptomaker.py`, it will return a code, your original message, and the encoded message.

```
user@computer:~/directory$ python cryptomaker.py Hello, World!

Your cryptogram code is:
A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
S  F  A  J  K  V  Q  W  M  C  O  U  D  I  P  B  N  G  L  R  X  E  Z  H  T  Y

Your original message was:
Hello, World!

Your new message is:
WKUUP, ZPGUJ!

Finished!
```

**In order to use `cryptomaker.py`, you must have the following installed:**
- python
- numpy
