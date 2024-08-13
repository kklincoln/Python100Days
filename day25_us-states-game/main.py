import turtle
import pandas

#create the turtle, screen, and adjust the screen background to the US state map
screen = turtle.Screen()
screen.title("United States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

#create state turtle
# def create_state(state,x_coord,y_coord):
#     state = turtle.Turtle()
#     state.penup()
#     # state.hideturtle()
#     state.shape("turtle")
#     state.goto(x_coord,y_coord)

#read 50 states csv and create a dictionary of states
data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                    prompt="What's another state's name?").title()
    # if answer_state == "Exit":
    #     missing_states = []
    #     for state in all_states:
    #         if state not in guessed_states:
    #             missing_states.append(state)
    #     new_data = pandas.DataFrame(missing_states)
    #     new_data.to_csv("States_to_Learn.csv")
    #     break
    #replace the code above with list comprehension
    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("States_to_Learn.csv")
        break
    # if user guesses state that exists, query the x and y coordinates
    elif answer_state in all_states:
        #append to the guessed states list
        guessed_states.append(answer_state)
        #create a turtle as the Title Case state name and move it to the x and y coordinates
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        # pull the data from the list and store in another variable
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer_state)



# #loop
# turtle.mainloop()