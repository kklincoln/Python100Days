import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

FONT = ("Arial",11)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    #Password Generator Project
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list = []

    password_letter = [choice(letters) for _ in range(nr_letters)]
    password_symbol = [choice(symbols) for _ in range(nr_symbols)]
    password_number = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_symbol + password_number
    shuffle(password_list)

    password = "".join(password_list)
    # print(f"Your password is: {password}")
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)    #auto-copies the password to the clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #

# call function to write to file
def save_pass():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "email": email,
            "password": password
        }

    }
    if len(website) == 0 or len(password) == 0 or len(email) ==0:
        messagebox.showerror(title="Error: Missing Information!",message="Please validate your entries, they cannot be blank.")
    else:
        # takes the website, email, password; saves them to a file with a space and pipe between each
        try:
            with open("password_file.json", "r") as pw_file:
                ## Reading from data and converting into a python dictionary from JSON object; update the open arg to "r"
                data = json.load(pw_file)
        except FileNotFoundError: #if file !exist, create and dump
            with open("password_file.json", "w") as pw_file:
                data = json.dump(new_data, pw_file, indent = 4)
        else: #if everything in Try is successful; update data from JSON; update the open arg to "w"
            data.update(new_data)

            with open("password_file.json", "w") as pw_file:
                ## writing updated data to json file with indents for readability
                json.dump(data, pw_file,indent =4)
        finally:
            # delete entry boxes upon writing
            website_entry.delete(0, END)
            # email_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus() #refocus toward website entry box
            # popup window indicating success/error


# --------------------------- USER SEARCH ------------------------------- #
def search_user():
    website_search = website_entry.get()
    # deal with exceptions (filenotfounderror)?
    try:
        with open("password_file.json", "r") as pw_file:
            data = json.load(pw_file)
    except FileNotFoundError:  # if file !exist, messagebox
        messagebox(title="Error: No File Found!", message="No user file exists, store credentials first.")
    else:
        if website_search in data: #if website key exists in current dictionary;
            found_email = data[website_search]['email'] # get the value associated with key: 'email'
            found_password = data[website_search]['password'] # get the value associated with the key: 'password'
            messagebox.showinfo(title="User Credentials", message=f"Credentials for {website_search}:\n"
                                                         f"Email Address: {found_email}\nPassword: {found_password}")
        elif len(website_search) ==0:
            messagebox.showinfo(title="Input Search Website", message="No website was provided to be searched upon,"
                                                                      " please provide one.")
        else:
            messagebox.showinfo(title="No Data Stored", message=f"No details exist for the {website_search} provided.")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator...")
window.config(padx=50, pady=50)

logo_path = "logo.png"

image_holder = Canvas(width=200, height=200)
logo_image = PhotoImage(file=logo_path)
image_holder.create_image(100, 100, image=logo_image)
image_holder.grid(row=0, column=0, columnspan=3)

# labels
website = Label(text="Website :")
website.grid(row=1, column=0)

email = Label(text="Email/username :")
email.grid(row=2, column=0)

password = Label(text="Password :")
password.grid(row=3, column=0)

# entry
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1,sticky="ew",padx=5,pady=3) # added padx and pady
website_entry.focus() #focuses the cursor into this box upon load

email_entry = Entry(width=45)
email_entry.grid(row=2, column=1,columnspan=2,sticky="ew",padx=5,pady=3) # added padx and pady
email_entry.insert(0, "kiernan.lincoln+passwordmanager@gmail.com") #inserts text at the index 0 character or END,

password_entry = Entry(width=21)
password_entry.grid(row=3,column=1,sticky="ew",padx=5,pady=3) # added padx and pady


#buttons
search_user_btn = Button(text="Search", command=search_user)
search_user_btn.grid(row=1, column=2, sticky="ew", padx=5, pady=3)

genrate_password_btn = Button(text="Generate Password",command=generate_password)
genrate_password_btn.grid(row=3, column=2,sticky="ew",padx=5,pady=3) # added padx and pady

add_button = Button(text="Add",width=40, command=save_pass)
add_button.grid(row=4, column=1,columnspan=2,sticky="ew",padx=5,pady=3) # added padx and pady


window.mainloop()

