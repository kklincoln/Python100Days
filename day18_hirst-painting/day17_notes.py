import turtle
from turtle import Turtle, Screen

tim = Turtle()
tim.shape("turtle")
tim.color("DarkSlateGray", "DarkSlateGray2")

#challenge 1 draw a 100 x 100 square
# for _ in range(4):
#     tim.forward(100)
#     tim.right(90)

#challenge 2: draw a dashed line; 10 paces blank 10 paces line, repeat 15x
# for _ in range (15):
#     tim.forward(10)
#     tim.penup()
#     tim.forward(10)
#     tim.pendown()

#challenge 3: draw a triangle, square,pentagon, hexagon, heptagon, octagon, nonagon, and decagon
# import random
# colors = ["FireBrick", "OrangeRed", "DarkGoldenrod1", "DarkOliveGreen", "SeaGreen", "DarkSlateGray4", "DeepSkyBlue4"]
# def draw_shape(num_sides):
#     angle = 360 / num_sides
#     for i in range(num_sides):
#         tim.forward(100)
#         tim.right(angle)
#     num_sides += 1
#
# for shape_side_n in range(3,11):
#     tim.color(random.choice(colors))
#     draw_shape(shape_side_n)

#challenge 4: Draw a random walk: different directions, same distance, same color palette as before
# import random
# # colors = ["FireBrick", "OrangeRed", "DarkGoldenrod1", "DarkOliveGreen", "SeaGreen", "DarkSlateGray4", "DeepSkyBlue4"]
# turtle.colormode(255)
# directions = [0, 90, 180, 270]
# tim.pensize(10)
# tim.speed(50)
#
#
# def random_color():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     random_color = (r, g, b)
#     return random_color
#
#
# for _ in range(200):
#     tim.color(random_color())
#     tim.forward(30)
#     tim.setheading(random.choice(directions))


# #challenge 5: draw a spirograph
# import random
# # colors = ["FireBrick", "OrangeRed", "DarkGoldenrod1", "DarkOliveGreen", "SeaGreen", "DarkSlateGray4", "DeepSkyBlue4"]
# turtle.colormode(255)
# tim.speed(50)
#
# def random_color():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     color = (r, g, b)
#     return color
#
# def draw_spirograph(size_of_gap):
#     for _ in range(int(360 / size_of_gap)):
#         current_heading = tim.heading()
#         tim.setheading(current_heading + size_of_gap)
#         tim.color(random_color())
#         tim.circle(100)
#
# draw_spirograph(5)





#keeps the screen open until clicked; keep at the bottom; mo
screen = Screen()
screen.exitonclick()