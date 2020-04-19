import json
import sys

from pathlib import Path
import pygame

WIDTH = 360
HEIGHT = 480
FPS = 30


class Maze(pygame.sprite.Sprite):
    """Class to store and display Maz e"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        try:
            p = Path('./ressources/maze.json')
            with open(p, 'r') as json_file:
                self.map = json.load(json_file)["maze"]
        except FileNotFoundError:
            print(f"File {p} do not exists, please check ressource folder")
            sys.exit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit()

    def draw(self):
        print(self.map)


class Sprite(pygame.sprite.Sprite):
    """ class for necessary for any sprite of the game"""


    def __init__(self, pos, image_path):
        super().__init__()
        self.pos = pos
        self.img = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()



# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#Initialize game classes
maze = Maze()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
