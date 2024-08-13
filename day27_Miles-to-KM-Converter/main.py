from tkinter import *

FONT =("Arial", 14)

window = Tk()
window.config(padx=20, pady=20)
window.title("Miles to Km Converter")
window.minsize(width=200, height=150)

#input: miles input text box
entry = Entry(font=FONT,width=10)
entry.insert(END, string="0")
entry.grid(column=2,row=1)

#label: miles
miles = Label(text="Miles", font=FONT)
miles.grid(column= 3,row=1)

#label: "is euqal to"
equals_label = Label(text="is equal to ", font=FONT)
equals_label.grid(column=1,row=2)

#label: conversion calculation result
result_label = Label(text="0", font=FONT)
result_label.grid(column=2,row=2)

#button click function
def convert():
    miles = float(entry.get())
    km = miles * 1.609
    result_label.config(text=f"{km}")

#label: km
km = Label(text="Km", font=FONT)
km.grid(column=3,row=2)

#calculate button
calc_btn= Button(text="Calculate", font=FONT, command=convert)
calc_btn.grid(column=2,row=3)




window.mainloop()