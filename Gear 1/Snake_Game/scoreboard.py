from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("high_score.txt") as f:
            self.high_score = int(f.read().split(":")[1])
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 280)  
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()  
        self.write(arg=f"Score = {self.score} High score: {self.high_score}", align='center', font=('Courier', 14, 'normal'))

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.highest_score()
        self.score = 0
        self.update_scoreboard()


    # def game_over(self):
    #     self.goto(0,0)  
    #     self.write(arg=f"Game over.", align='center', font=('Courier', 24, 'normal'))

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def highest_score(self):
        with open("high_score.txt", mode="w") as f:
            f.write(f"high_score: {self.high_score}")

