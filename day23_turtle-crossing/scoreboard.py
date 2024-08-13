from turtle import Turtle

FONT = ("Arial", 16, "normal")
ALIGNMENT = "Left"

class Scoreboard(Turtle):
    # DONE: Step 7 create a scoreboard that tracks the level the user is on; increase with each finish_line pass
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("Black")
        self.penup()
        self.goto(-280,250)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Current Level: {self.score}", align = ALIGNMENT,font = FONT )

    def increase_score(self):
        self.score +=1
        self.clear()
        self.update_scoreboard()

    def game_over(self):
        self.goto(0,0)
        self.write(f"Game over! Total Score: {self.score}", align = "center",font = FONT )
