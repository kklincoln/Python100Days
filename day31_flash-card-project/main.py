from tkinter import messagebox,Tk,Canvas,PhotoImage,Button,Grid
import pandas
import random

TITLE=("Arial",40,"italic")
WORD=("Arial", 60, "bold")
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---READ FOREIGN WORDS DATA ---#
try:
    data = pandas.read_csv("data/words_to_learn.csv")  # prints as a dataframe
except FileNotFoundError:
   original_data = pandas.read_csv("data/french_words.csv")  # prints as a dataframe
   to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records") # orient formats dict as list [{'French':'partie', 'English':'part'},{}]

#------------------------------ KEY FUNCTIONS ------------------------------------#

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer) #cancels any previously running timeclock and resets it at the end with fx end line
    current_card = random.choice(to_learn) #dictionary pulled from the to_learn list
    #set the text associated with the variables for card title and word = to the card set
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    window.after(3000,flip_card)

def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="White")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background,image=card_back_image)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    #save progress
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index =False) #doesn't add index to the lists which affects read
    next_card()


#-----------------------------UI CODE----------------------------------------------#
window = Tk()
window.title("Flashy")
#background is 800card +50px padding; height = card height526 + 50px padding +button heights 100px
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR, width=900,height=900)
#3s delay then display the english translation
flip_timer = window.after(3000, func=flip_card) #3000ms

#card canvas
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400,263, image=card_front_image) #image position is half of the canvas
card_title = canvas.create_text(400,150,text="", font=TITLE)
card_word = canvas.create_text(400,263,text="", font=WORD)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


#buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_btn = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_btn.grid(row=1, column=0)
check_image = PhotoImage(file="images/right.png")
check_btn = Button(image=check_image, highlightthickness=0, command=is_known)
check_btn.grid(row=1,column=1)




#---------------------------------------------------------------------------#
#show the first card rather than the title
next_card()
window.mainloop()