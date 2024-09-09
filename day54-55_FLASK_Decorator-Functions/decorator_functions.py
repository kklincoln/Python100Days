import time
current_time = time.time()
print(current_time) #seconds since jan 1st, 1970

def speed_calc_decorator(function):
    def wrapper(*args, **kwargs):
        start_time = current_time
        result = function(*args, **kwargs)
        finish_time = current_time
        print(f"{function.__name__} run speed: {finish_time - start_time}s")
        return result
    return wrapper

@speed_calc_decorator
#given
def fast_function():
    for i in range(1000000):
        i*i
@speed_calc_decorator

def slow_function():
    for i in range(10000000):
        i*i




# from time import sleep
#
# #Building the first web server with flask
# from flask import Flask
# #__name__ referring to calling the name of the library, currently it's __main__ bc it's built here
# app = Flask(__name__)
#
# #only trigger the decorator funciton IF the user is trying to access the homepage with the / symbol appended
# @app.route('/')
# def hello_world():
#     return 'Hello, world!'
#
# #only runs if the user is trying to access the page: homepage/bye
# @app.route('/bye')
# def say_bye():
#     return "Bye"
#
# #-------------------------- NOTES -----------------------#
# def delay_decorator(function):
#     def wrapper_function():
#         sleep(2)
#         function() #calls the function from the argument
#     return wrapper_function
#
# @delay_decorator
# def say_hello():
#     print("Hello")
#
# @delay_decorator #adds the several second delay from the wrapper function
# def say_bye():
#     print("Goodbye")
#
# def say_greeting():
#     print("how are you?")
#
# decorated_function = delay_decorator(say_greeting)
# decorated_function() #this achieves the same result as the @delay_decorator approach, but less efficiently
