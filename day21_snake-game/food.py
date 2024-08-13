from turtle import Turtle
import random

class Food(Turtle):
    def __init__(self):
        super().__init__() #needs to be declared when initializing the Turtle class inheritance
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5) #shrink the food size from 20x20 to 10x10
        self.color("blue")
        self.speed("fastest")
        random_x = random.randint(-280,280)
        random_y = random.randint(-280,280)
        self.goto(random_x, random_y)

    def refresh(self):
        random_x = random.randint(-280,280)
        random_y = random.randint(-280,280)
        self.goto(random_x, random_y)