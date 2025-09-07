from turtle import Screen
import time
from player import Player
from car_manager import CarManager
from scoreboard import ScoreBoard
from music import Music

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
score_board = ScoreBoard()
music = Music()

screen.listen()
screen.onkey(player.move, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move()

    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            score_board.game_over()
            music.lost_sound()
            game_is_on = False
    
    if player.is_at_finish_line():
        music.level_up_sound()
        player.go_to_start()
        car_manager.level_up()
        score_board.increase_level()
        
screen.exitonclick()
