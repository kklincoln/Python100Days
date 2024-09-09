from flask import Flask

app = Flask(__name__)

@app.route('/')  # decorator function living in the app object, which is declared in the Flask class
def say_hello():
    return ('<h1 style="text-align: center">Hello, World!</h1>' 
            '<p>That guess is too low. Try again!</p>'
            '<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGFoeDI2bmkydzhnaWFoMmd5d3FsYX'
            'JrbGxlaHNwN3NqY3ZwbTc1eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rS2uLYRGkGWySNX69v/giphy.gif">'
            )  # Return a valid HTTP response

#wrapper function to make something bold
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

#when navigating to homepage/bye:
@app.route('/bye')
#since these were built here, you don't need to prefix with app.
@make_bold
@make_emphasis
@make_underline
def say_bye():
    return "Goodbye"

#creating variable paths and converting the path to a specified data type
#when navigating to a page with the username/<name> variable, the page will greet the variable
@app.route('/username/<name>/<int:number>')
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"

if __name__ =="__main__":
    #run the app in debug mode to auto-reload server
    app.run(debug=True)

#----------------------------------------------------------------------------------#
#----------------------- advanced python decorator functions-----------------------#

class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    #use the *args, **kwargs section to indicate that the arguments are passed in elsewhere
    def wrapper(*args, **kwargs):
        #looks at the function passed in, then references the argument at index 0 for use
        if args[0].is_logged_in == True:
            #passing in that same argument representing User into the create_blog_post function
            function(args[0])
    return wrapper

#call the is_authenticated_decorator prior to create blog_post, only calls function if True
@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


#create a new instance of the user class with my name
new_user = User("Kiernan")
create_blog_post(new_user)


#-------------------------------example code-----------------------------------------------#
#create a logging_decorator() which is going to print the name of the function called, the arguments, and the result
def logging_decorator(function):
    def wrapper(*args,**kwargs):
        print(f"You called {function.__name__}{args}")
        result = function(args)
        print(f"The result was: {result}")
        return result
    return wrapper

@logging_decorator
def a_function(*args):
    return sum(args)

a_function(1,2,3)