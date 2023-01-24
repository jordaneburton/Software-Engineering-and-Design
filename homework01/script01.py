word1 = "" #initialize our five longest words
word2 = ""
word3 = ""
word4 = ""
word5 = ""

words = []

with open('/usr/share/dict/words', 'r') as f:
    words = f.read().splitlines()                # careful of memory usage

for word in words:
    if (len(word) > len(word1)):
        word5 = word4
        word4 = word3
        word3 = word2
        word2 = word1
        word1 = word
    elif (len(word) > len(word2)):
        word5 = word4
        word4 = word3
        word3 = word2
        word2 = word
    elif (len(word) > len(word3)):
        word5 = word4
        word4 = word3
        word3 = word
    elif (len(word) > len(word4)):
        word5 = word4
        word4 = word
    elif (len(word) > len(word5)):
        word5 = word

words = [word1, word2, word3, word4, word5]
print(words)
