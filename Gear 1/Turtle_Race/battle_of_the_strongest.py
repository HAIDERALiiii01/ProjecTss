from turtle import Turtle, Screen
import random, time

s = Screen()
s.setup(width=500, height=400)
s.title("Turtle Color Race")

def intro():
    return s.textinput(title="Your Prediction", prompt="Which color will win the race?\n(Choose from: red, blue, green, yellow, purple, black)").strip().lower()

# Get user's prediction
prediction = intro()

# List of turtle colors and their starting y-positions
values = [
    {"color": "yellow", "position": -70},
    {"color": "red", "position": -40},
    {"color": "purple", "position": -10},
    {"color": "blue", "position": 20},
    {"color": "green", "position": 50},
    {"color": "black", "position": 80},
]

all_turtles = []

# Create turtles with colors only
for val in values:
    t = Turtle(shape="turtle")
    t.color(val["color"])
    t.penup()
    t.goto(x=-230, y=val["position"])
    all_turtles.append({"turtle": t, "color": val["color"]})

# Turtle to display result only
result_writer = Turtle()
result_writer.hideturtle()
result_writer.penup()
result_writer.goto(0, 150)

# Start race if prediction is provided
is_race_on = bool(prediction)

while is_race_on:
    for entry in all_turtles:
        t = entry["turtle"]
        t.forward(random.randint(0, 10))

        if t.xcor() > 230:
            is_race_on = False
            winner_color = entry["color"]
            if prediction == winner_color:
                result_writer.write(f"You won! {winner_color.capitalize()} turtle is the winner!", align="center", font=("Arial", 14, "bold"))
            else:
                result_writer.write(f"You lost! {winner_color.capitalize()} turtle is the winner!", align="center", font=("Arial", 14, "bold"))
            break

s.exitonclick()
