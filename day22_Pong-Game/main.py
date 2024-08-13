# TODO: CREATE THE SCREEN
    # TODO: MIDDLE DASHED DIVIDER
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
import time
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.screensize(800,600)
screen.title("PONG")
screen.tracer(0) #turns animations off

r_paddle = Paddle((430,0))
l_paddle = Paddle((-430,0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
# TODO: RIGHT (USER) PADDLE
screen.onkey(r_paddle.go_up,"Up")
screen.onkey(r_paddle.go_down,"Down")

# TODO: LEFT (COMPUTER) PADDLE
screen.onkey(l_paddle.go_up,"w")
screen.onkey(l_paddle.go_down,"s")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    # TODO: PONG BALL THAT MOVES
    ball.move()

    # TODO: DETECT COLLISION WITH WALL
    if ball.ycor() > 375 or ball.ycor() < -375:
        #bounce the ball
        ball.bounce()

    # TODO: DETECT COLLISION WITH PADDLE
        #If paddle crosses a x_pos AND within 50px of paddle, it hits
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 410) or (ball.distance(l_paddle) < 50 and ball.xcor() < -410):
        ball.change_direction()

    # TODO: DETECT R PADDLE MISS
    if ball.xcor() > 450:
        ball.reset_position()
        scoreboard.l_point()

    # TODO: DETECT L PADDLE MISS
    if ball.xcor() < -450:
        ball.reset_position()
        scoreboard.r_point()


screen.exitonclick()