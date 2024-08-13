from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

# TODODone: create a turtle player that starts at the bottom of the screen;
class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.color("red","orange")
        self.goto(STARTING_POSITION)
        self.setheading(90)
        self.x_position =0
        self.y_position =-280

    # DONE: CREATE MOVE Method
    def move_up(self):
        self.forward(MOVE_DISTANCE)
    def move_down(self):
        new_y = self.ycor() - MOVE_DISTANCE
        self.goto(self.x_position, new_y)
    # def move_left(self):
    #     self.x_position -= MOVE_DISTANCE
    # def move_right(self):
    #     self.x_position += MOVE_DISTANCE

    # DONE: CREATE reset_position Method (run over or level up)
    def reset_position(self):
        self.goto(STARTING_POSITION)

    # DONE:  step 6 detect when the player has reached the top edge of the screen (FINISH_LINE_Y). when this happens
    # return the turtle to the starting position; increase speed of cars (create attribute and use MOVE_INCREMENT)
    def is_at_finish_line(self):
        return self.ycor() > 280

