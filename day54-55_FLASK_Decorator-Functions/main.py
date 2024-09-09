import random
from flask import Flask

random_number = random.randint(0,9)
print(random_number)

app = Flask(__name__)

@app.route('/')  # decorator function living in the app object, which is declared in the Flask class
def home():
    return('<h1 style="text-size=16"> Guess a number between 0 and 9</h1>'
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">')  # Return a valid HTTP response


#when navigating to homepage/bye:
@app.route('/<int:guess>')
def say_bye(guess):
    if guess < random_number:
        return ('<h1 style="text-align: center">Too Low!</h1>'
                '<p>That guess is too low. Try again!</p>'
                '<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGFoeDI2bmkydzhnaWFoMmd5d3FsYX'
                'JrbGxlaHNwN3NqY3ZwbTc1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rS2uLYRGkGWySNX69v/giphy.gif">'
                )
    elif guess > random_number:
        return ('<h1 style="text-align: center">Too High!</h1>'
                '<p>That guess is too damn high. Try again!</p>'
                '<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2h2aWg2cmpobnpwc3pqaWUxcm03YWt1OGd3bmNjcGlsMX'
                'pxbnQzayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MwrQvTZA9Puuc/giphy.gif">'
                )
    else: # number == random_number:
        return ('<h1 style="text-align:center">Right on the Money!</h1>'
                '<p>You got the right answer!</p>'
                '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjg4a2owY2l0bDd6c3R0NzR'
                'oMHFrdHBwdTd1NmMwMGowMm9xNnI5eCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Vq9ortuhLZy3obaEFy/giphy.gif">')

#creating variable paths and converting the path to a specified data type
#when navigating to a page with the username/<name> variable, the page will greet the variable
if __name__ =="__main__":
    #run the app in debug mode to auto-reload server
    app.run(debug=True)
