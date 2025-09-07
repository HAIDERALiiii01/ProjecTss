from turtle import Turtle

font_for_game_over = ("Courier", 24, "normal")
font_for_level = ("Courier", 15, "normal")

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.current_level = 1
        self.color("black")
        self.penup()
        self.hideturtle()
        self.goto(-220, 260)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Level: {self.current_level}", move=False, align="left", font=font_for_level)

    def game_over(self):    
        self.goto(0, 0)
        self.write("GAME OVER", move=False, align="center", font=font_for_game_over)

    def increase_level(self):
        self.current_level += 1
        self.update_scoreboard()

