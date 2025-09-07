from turtle import Turtle, Screen 
import pandas

turtle = Turtle()
t = Turtle()
screen = Screen()

screen.title("U.S States Game")
shape = "blank_states_img.gif"
# screen.setup(width=800, height=800) 
screen.addshape(shape)
turtle.shape(shape)

t.penup()
t.hideturtle()
t.color("black")

data = pandas.read_csv("50_states.csv")
states_in_list = data["state"].to_list()
# print(states_in_list[0])
x_cordinates_in_list = data["x"].to_list()
# print(x_cordinates_in_list[0])
y_cordinates_in_list = data["y"].to_list()
# print(y_cordinates_in_list[0])


total_states = 50
guessed_states = [] 
score = 0

while len(guessed_states) < 50:
    answer_input_not_cleaned = screen.textinput(title = f"Guess the state({len(guessed_states)}/50)", prompt = "What's is another state's name")
# state_data = data[data.state == answer_input]
# t.goto(data.x.item(), data.y.item())
    if answer_input_not_cleaned is not None:
        answer_input = answer_input_not_cleaned.title()
        if answer_input in states_in_list:
            guessed_states.append(answer_input)
            index = states_in_list.index(answer_input)
            x = x_cordinates_in_list[index]
            y = y_cordinates_in_list[index]
            t.goto(x,y)
            t.write(answer_input, align="center", font=("Arial", 8, "normal"))

            
            score += 1
        elif answer_input == "Exit":
            missing_states = [state for state in states_in_list if state not in guessed_states]
            # missing_states = []
            # for state in states_in_list:
            #     if state not in guessed_states:
            #         missing_states.append(state)
            # print(missing_states)
            new_data = pandas.DataFrame(missing_states)
            new_data.to_csv("missing__states.csv")
            break

        else:
            pass
    else:
        answer_input = None
        break




# screen.exitonclick()