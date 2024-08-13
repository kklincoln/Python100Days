from tkinter import *

#creating the function that will be executed by the button
def button_clicked():
    new_text = input.get()
    my_label.config(text=new_text)
    print("I got clicked")

def button2_clicked():
    new_text2 = input.get()
    my_label.config(text=new_text2)
    print("Second button clicked")

#similar to the "screen" class in turtle
window = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20) #adds padding around the window border

#label class
my_label = Label(text = "I am a label", font=("Arial", 24, "bold"))
my_label.config(text="New Text",padx=10, pady=10)
#specify how the label will appear on the screen
my_label.grid(column=1, row=1)

#creating a button
button = Button(text="Click me", command=button_clicked)
button.grid(column=2, row=2)

#creating a new button
button2 = Button(text="Second Button", command=button2_clicked)
button2.grid(column=3, row=1)

#creating text entry box
input = Entry(width=10)
input.grid(column=4, row=4)





window.mainloop()