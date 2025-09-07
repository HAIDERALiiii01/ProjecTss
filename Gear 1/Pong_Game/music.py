import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sss.mp3')
        pygame.mixer.music.play(loops=-1)  # Background music in loop