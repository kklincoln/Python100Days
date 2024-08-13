import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0) #turns off the auto refresh
scoreboard  = Scoreboard()

# DONE create a turtle player that starts at the bottom of the screen;
player1 = Player()
# DONE: step 3 Listen for the "up" keypress to move the turtle north.
screen.listen()
screen.onkey(player1.move_up,"Up")
screen.onkey(player1.move_down,"Down")

# DONE: step 4 create cars that are 30px x 40px randomly generated across the y-axis and move to the left side;
car_manager = CarManager()

game_is_on = True
while game_is_on:
    time.sleep(0.1) #updates the code via loop every 0.1 seconds
    screen.update()
    car_manager.create_car()
    car_manager.move_car()

    # DONE:  step 5 detect when the turtle player collides with a car and stop the game if this happens.
    for car in car_manager.all_cars:
        if car.distance(player1) < 20:
            player1.reset_position()
            car_manager.level_up()
            game_is_on = False
            scoreboard.game_over()

    # DONE:  step 6 detect when the player has reached the top edge of the screen (FINISH_LINE_Y). when this happens
    # return the turtle to the starting position; increase speed of cars (create attribute and use MOVE_INCREMENT)
    if player1.is_at_finish_line():
        player1.reset_position()
        # DONE: Step 7 create a scoreboard that tracks the level the user is on; increase with each finish_line pass
        scoreboard.increase_score()

screen.exitonclick()