from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width= 600,height= 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0) # turn off the tracer that shows the lag between the segments

snake = Snake()
food = Food()
scoreboard = Scoreboard()

#Done: control the snake with arrow keys
# after the snake is created, listen for directional cues
screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")

game_is_on = True
while game_is_on:
    screen.update() # keep the update screen feature outside forloop so that it only updates once all seg moved
    time.sleep(0.1)
    snake.move()

    #TODO: detect collision with food and add to length; needs to be nested within while above
    # if the snake head is within 15px, perform action
    if snake.head.distance(food) < 15:
        food.refresh()
        # TODO: update the score
        scoreboard.add_point()
        snake.extend()

    #TODO: detect collision with wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        scoreboard.reset()
        snake.reset()

    #TODO: detect collision with body
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset()
            snake.reset()

screen.exitonclick()