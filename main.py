import json
import sys

from random import randint

from pathlib import Path
import pygame

#Main parameter for pygame window
#dimensions in pixel
WIDTH = 640
HEIGHT = 640
WIDTH_OPTION = 40
HEIGHT_OPTION  = 40
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
        self.items = self.__init_objects()

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
            if (self.compare_sprite((x,y), "floor") and
                not self.guardian.compare_pos((x,y))):
                results.append(Sprite(assets[sprite[len(results)]], (x*40, y*40)))
        return results

    def compare_sprite(self, pos, sprite_name):
        """ Compare sprite in pos with the sprite given
        return a boolean"""
        if (self.map[pos[0]+pos[1]*15].image == assets[sprite_name]):
            return True
        return False

class Player(Sprite):
    """Special Sprite with additional function to allow movement depending on key press by player"""
    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.moving = False
        self.target = [pos[0], pos[1]]
        self.speed = [0,0]
        self.alive = True
        self.escape = False
        self.items = []


    def update(self):
        if self.moving:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            if self.target == [self.rect.x, self.rect.y]:
                self.moving = False
                self.speed[0] = 0
                self.speed[1] = 0
        else:
            self.check_guardian()
            if len(self.items) < 3:
                self.check_objects()
            else:
                self.items.append(Sprite(assets["syringe"], (5*40,15*40)))
                #to be modify
                all_sprites.add(self.items[3])
            self.check_mov()

    def check_guardian(self):
        """ Check if guardian if guardian is in cell and depending on number of objects in possession of player
        kill guardian or player"""
        if (maze.guardian.rect.x == self.rect.x and 
        maze.guardian.rect.y == self.rect.y):
            if len(self.items) == 3:
                self.escape = True
            else:
                self.alive = False

    def check_objects(self):
        for i,item in enumerate(maze.items[:]):
            if (item.rect.x == self.rect.x and
            item.rect.y == self.rect.y):
               self.items.append(maze.items.pop(i))
               #Modify position of items to place it our of maze
               index = len(self.items) - 1
               self.items[index].rect.x = index * 40
               self.items[index].rect.y = 15 * 40
               #Not possible to have two items on same place so there is no need to continue test
               break

    def check_mov(self):
        """fonction that check the validity of move of the player and change target, speed and movement status if movement allow"""
        keystate = pygame.key.get_pressed()
        if (keystate[pygame.K_LEFT] and
        self.rect.left > 0 and
        maze.compare_sprite(self.pos_left(), "floor")):
            self.target[0] -= 40
            self.speed[0] = -10
            self.moving = True

        if (keystate[pygame.K_RIGHT] and
        self.rect.right < WIDTH - WIDTH_OPTION and 
        maze.compare_sprite(self.pos_right(), "floor")):
            self.target[0] += 40
            self.speed[0] = +10
            self.moving = True

        if (keystate[pygame.K_UP] and
        self.rect.top > 0 and
        maze.compare_sprite(self.pos_up(), "floor")):
            self.target[1] -= 40
            self.speed[1] = -10
            self.moving = True

        if (keystate[pygame.K_DOWN] and
        self.rect.bottom < HEIGHT - HEIGHT_OPTION and
        maze.compare_sprite(self.pos_down(), "floor")):
            self.target[1] += 40
            self.speed[1] = +10
            self.moving = True

    def pos_left(self):
        """Return tuple of index from sprite at the left of player """
        return ((self.rect.x-40)//40, self.rect.y//40)


    def pos_right(self):
        """Return tuple of index from sprite at the left of player """
        return ((self.rect.x+40)//40, self.rect.y//40)


    def pos_up(self):
        """Return tuple of index from sprite at the left of player """
        return (self.rect.x//40, (self.rect.y-40)//40)


    def pos_down(self):
        """Return tuple of index from sprite at the left of player """
        return (self.rect.x//40, (self.rect.y+40)//40)


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
player = Player(assets["player"], (2*40, 1*40))

#Load Sprites in group
all_sprites = pygame.sprite.Group()
for sprite in maze.map:
    all_sprites.add(sprite)
all_sprites.add(maze.guardian)
for sprite in maze.items:
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

    if player.escape:
        running = False
        print("You Win")

    if not player.alive:
        running = False
        print("You Lose")

    # Update all sprites status
    all_sprites.update()

    # Draw / render
    screen.fill((0,0,0))
    all_sprites.draw(screen)

    #Display changes on screen
    pygame.display.flip()

pygame.quit()
