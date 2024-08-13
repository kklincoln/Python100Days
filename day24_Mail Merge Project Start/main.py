#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

# constant to be replaced
PLACEHOLDER = "[name]"

#TODO: open invites and save to variable; txt.readlines (returns names as list format with '\n' appended
with open("input/names/invited_names.txt") as invites:
    names = invites.readlines()

# TODO: open starting letter and save to variable
with open("input/letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    # TODO: for loop for each name in the names file to replace the carriage return with a comma
    for name in names:
        stripped_name = name.strip()
        new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)
        # TODO: file.write() to new output files for each of the stripped_name
        with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.docx", mode="w") as completed_letter:
            completed_letter.write(new_letter)





