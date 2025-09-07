import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('main.mp3')
        pygame.mixer.music.play(loops=-1)  # Background music in loop

    def lost_sound(self):
        pygame.mixer.music.stop()  # Stop background music
        sound = pygame.mixer.Sound('game_over.mp3')
        sound.play()

    def level_up_sound(self):
        sound = pygame.mixer.Sound('leveup.mp3')
        sound.play()
