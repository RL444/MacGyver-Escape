import json
import sys

from random import randint

from pathlib import Path
import pygame

#Main parameter for pygame window
#dimensions in pixel
WIDTH = 640
HEIGHT = 640
FPS = 30

def load_assets(folder_path):
    """Load and convert all png file of a folder into a dictionnary to be returned"""
    storage = {}
    for path in folder_path.glob('*.png'):
        storage[path.stem] = pygame.image.load(str(path)).convert()

    return storage

class Sprite(pygame.sprite.Sprite):
    """Class to manage sprite of the game with minimal information required"""
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def compare_pos(self, pos):
        """ Compare position of this sprite with position in parameter 
        return a boolean"""
        if self.rect.x == pos[0] and self.rect.y == pos[1]:
            return True
        return False


class Maze:
    """Class to manage status of the maze"""
    def __init__(self, folder_path):
        super().__init__()
        #Load map, create a list of Sprite instance corresponding to the status wall or floor with right position
        self.map = self.__init_map(folder_path)
        self.guardian = Sprite(assets["guardian"],(14*40,8*40))
        self.objects = self.__init_objects()

    def __init_map(self, folder_path):
        """Load map and create Sprite instance for background
        return a list of Sprite"""
        result = []
        folder_path = folder_path / 'maze.json'
        with open(str(folder_path), 'r') as json_file:
            data = json.load(json_file)
            for row, line in enumerate(data["maze"]):
                for column, val in enumerate(line):
                    if int(val):
                        result.append(
                            Sprite(assets["floor"], (column*40, row*40)))
                    else:
                        result.append(
                            Sprite(assets["wall"], (column*40, row*40)))
        return result

    def __init_objects(self):
        """Create sprite for the 3 pickable objects with random position inside the maze, avoiding wall and guardian position
        return list of the 3 sprites"""
        results = []
        sprite = ["plastic_tube", "ether", "needle"]
        while len(results) < 3:
            x = randint(0, 14)
            y = randint(0, 14)
            if (self.map[x+y*15].image == assets["floor"] and
                not self.guardian.compare_pos((x,y))):
                results.append(Sprite(assets[sprite[len(results)]], (x*40, y*40)))
        return results

class Player(Sprite):
    """Special Sprite with additional function to allow movement depending on key press by player"""
    def __init__(self, img, pos):
        super().__init__(img, pos)


    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -= 40
        if keystate[pygame.K_RIGHT]:
            self.rect.x += 40
        if keystate[pygame.K_UP]:
            self.rect.y -= 40
        if keystate[pygame.K_DOWN]:
            self.rect.y += 40
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top  < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


# initialize pygame and create Game Window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#Load assets
ressources = Path(".").joinpath("ressources")
assets = load_assets(ressources)

#Instance for main classes
maze = Maze(ressources)
player = Player(assets["player"], (1*40, 1*40))

#Load Sprites in group
all_sprites = pygame.sprite.Group()
for sprite in maze.map:
    all_sprites.add(sprite)
all_sprites.add(maze.guardian)
for sprite in maze.objects:
    all_sprites.add(sprite)
all_sprites.add(player)

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

    # Update all sprites status
    all_sprites.update()

    # Draw / render
    screen.fill((0,0,0))
    all_sprites.draw(screen)

    #Display changes on screen
    pygame.display.flip()

pygame.quit()
