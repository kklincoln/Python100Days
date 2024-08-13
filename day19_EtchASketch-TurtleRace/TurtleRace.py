import turtle
from turtle import Turtle, Screen
import random

screen = Screen()
is_race_on = False
# dimensions of the screen are crucial, so use the setup method
screen.setup(width =500, height= 400)
#create a popup window that allows the user to provide input
user_bet = screen.textinput(title="Make Your Bet!", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

# position the turtles on the very left side of the screen
#TODO Create forloop to create 6 turtles of colors in colors array and position them along the left side of the screen
for turtle_index in range(0, len(colors)):
    new_turtle = Turtle("turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.speed(random.randint(0, 100))
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True

while is_race_on == True:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")
        random_distance =  random.randint(0,10)
        turtle.forward(random_distance)

screen.exitonclick()