def getSmallestString(word, substr):
    def replace_and_create(word, substr, pos):
 /* replace the '?' in the word with 'a' and insert substr at the specified pos*/
    new_word = list(word)
    new_word[pos: pos+ len(su
ibstr)]= substr