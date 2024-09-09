from tkinter import *
import requests

#api: https://api.kanye.rest
def get_quote():
    #make a get() request to the kanye rest API
    response = requests.get("http://api.kanye.rest")
    #raise an exception if the request returned an unsuccessful status code
    response.raise_for_status()
    # parse the JSON to obtain the quote text
    data = response.json()
    ye_quote = response.json()["quote"]
    print(ye_quote)
    # display the quote in the canvas' quote_text widget
    canvas.itemconfig(quote_text,text=ye_quote)


window = Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(150, 207, text="Kanye Quote Goes HERE", width=250, font=("Arial", 30, "bold"), fill="white")
canvas.grid(row=0, column=0)

kanye_img = PhotoImage(file="kanye.png")
kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(row=1, column=0)



window.mainloop()