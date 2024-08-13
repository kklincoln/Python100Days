from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

def move_forward():
    tim.forward(10)
def move_backward():
    tim.backward(10)
def turn_clockwise():
    tim.right(10)
def turn_counterclockwise():
    tim.left(10)
def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

# to start listening to events, we need to tell the screen object to start listening
screen.listen()
# to bind a keystroke to an event in our code, we need to have to use event listeners, in this case, onkey()
#note, we don't add the parentheses on the function since we don't want it trriggered right then and there
#TODO 1: create a movement pattern for w:forward; s:backward; a:rotate counter-clockwise; d:rotate clockwise; c-clear
screen.onkey(key = "w", fun = move_forward)
screen.onkey(key = "s", fun = move_backward)
screen.onkey(key = "a", fun = turn_clockwise)
screen.onkey(key = "d", fun = turn_counterclockwise)
screen.onkey(key = "c", fun = clear)

screen.exitonclick()
