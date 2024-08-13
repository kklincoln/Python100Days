###This code will not work in repl.it as there is no access to the colorgram package here.###
##We talk about this in the video tutorials##
import turtle

import colorgram #library of code that lets you extract colors from images

### code to gather the colors from cologram
# rgb_colors = []
# colors = colorgram.extract('image.jpg', 30)
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_colors.append(new_color)
# print(rgb_colors)

###### Print the hirst painting
import random
from turtle import Turtle, Screen
tim = Turtle()
tim.shape("turtle")
tim.speed(100)
tim.hideturtle()
tim.penup()
number_of_dots = 100
color_list = [(202, 164, 110), (149, 75, 50), (222, 201, 136), (53, 93, 123), (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102)]

turtle.colormode(255)
tim.setheading(225)
tim.forward(250)
tim.setheading(0)

# for y in range(10):
for dot_count in range (1, number_of_dots + 1):
    tim.dot(20,random.choice(color_list))
    tim.forward(50)

#once dot count reaches 10 on a row, reset to horizontal position and above by 50
    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)




#keeps the screen open until clicked; keep at the bottom; mo
screen = Screen()
screen.exitonclick()