from flask import Flask

#app is the homepage
app = Flask(__name__)
#the __name__ will be __main__ because we write the code in this file
if __name__ =="__main__":
    #run the app in debug mode to auto-reload server
    app.run(debug=True)

# HTML WRAPPER FUNCTIONS
def make_bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def make_emphasis(func):
    def wrapper(*args,**kwargs):
        return f"<em>{func(*args, **kwargs)}</em>"
    return wrapper

def make_underline(func):
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args,**kwargs)}</u>"
    return wrapper

#
# @app.route('/')  # decorator function living in the app object, which is declared in the Flask class
# @make_bold
# def ask_question():
#     return ('Hello')


@app.route('/')  # decorator function living in the app object, which is declared in the Flask class
def say_hello():
    return ('<h1 style="text-align: center">Hello, World!</h1>' 
            '<p>That guess is too low. Try again!</p>'
            '<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGFoeDI2bmkydzhnaWFoMmd5d3FsYX'
            'JrbGxlaHNwN3NqY3ZwbTc1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rS2uLYRGkGWySNX69v/giphy.gif">'
            )  # Return a valid HTTP response
