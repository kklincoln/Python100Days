import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

phoenetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(phoenetic_dict)

def generate_phonetic():
    word = input("Enter a word: ").upper()
    #catch the keyerror when a user enters a character that is not in the dictionary,
    try:
        code = [phoenetic_dict[letter] for letter in word]
    except KeyError:
        # provide feedback to the user when an illegal word was entered
        print("Sorry, only letters in the alphabet please.")
        # continue prompting the user to enter another word until they enter a valid word
        generate_phonetic()
    else:
        print(code)

generate_phonetic()


