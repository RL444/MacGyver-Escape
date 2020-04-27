import json

import pygame
from pathlib import Path

import init


class Game:
    """ Class managing the state machine and general information of the Game"""
    def __init__(self):
        # Initialize Pygame basics
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

        self.status = init.MENU

        # Load all information
        self.__load_data()

    def __load_assets(self, folder, files):
        """Load and convert all required png file of the folder
        return a dict of the surface created"""
        storage = {}
        try:
            for path in [folder / str(name + ".png") for name in files]:
                storage[path.stem] = pygame.image.load(str(path)).convert()
        except RuntimeError as error:
            print(error)
            self.status = init.EXIT

        return storage

    def __load_data(self):
        """load all data from data.json file in ressources folder
        in order to initialyse the needed class instances properly
        abort program if files do not exists"""
        # variable to contain all sprites
        self.all_sprites = pygame.sprite.Group()

        ressources = Path('.') / "ressources"
        try:
            with open(str(ressources / 'data.json'), 'r') as json_files:
                data = json.load(json_files)
                # Load all sprites inside a list for easy access
                self.assets = self.__load_assets(ressources,
                                                 data['List of sprites'])
                # Load map of the maze store inside data.json, also contain
                # position for Player and Guardian
                maze = data['maze']

                # Initialize player
                index = maze.index('P')
                self.player = Player(self.assets['player'],
                                     (index % 15, index // 15))

                # Initialize Maze
                self.maze = Maze(maze, self.assets)

                # Add sprite in sprite_group
                for sprite in self.maze.map.values():
                    self.all_sprites.add(sprite)
                self.all_sprites.add(self.maze.guardian)
                self.all_sprites.add(self.player.sprite)

        except (FileNotFoundError, FileExistsError) as error:
            print(error)
            print("Please check ressource folder before playing Game")
            self.status = init.EXIT
        except KeyError as error:
            print(f"error while attempting to read {error}" +
                  "from data.jon file")
            self.status = init.EXIT

    def run(self):
        """function used to mange the game display and behavior"""
        while self.status:
            # Keep loop running at the right speed
            self.clock.tick(30)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.status = init.EXIT

            # Display depending on game status
            if self.status == init.MENU:
                print("Menu")
                self.status = init.PLAY

            elif self.status == init.PLAY:
                self.screen.fill(init.BLACK)
                self.all_sprites.update()
                self.all_sprites.draw(self.screen)
                pygame.display.flip()

            elif self.status == init.FINISH:
                print("Finish")
                self.status = init.EXIT

        pygame.quit()


class Sprite(pygame.sprite.Sprite):
    """Enhanced Sprite with functions to ease computation"""
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * init.SPRITE_W, pos[1] * init.SPRITE_H)
        self.image.set_colorkey(init.BLACK)

    @property
    def pos(self):
        """Return tuple position of sprite after conversion from pixel
        to index referential"""
        return (self.rect.topleft[0]//init.SPRITE_W,
                self.rect.topleft[1]//init.SPRITE_H)

    @pos.setter
    def pos(self, pos):
        """Set position of sprite in pixel from index tuple"""
        self.rect.topleft = (pos[0]*init.SPRITE_W, pos[1]*init.SPRITE_H)


class Player:
    """Class to control the player movement, display
    and status inside the game"""
    def __init__(self, img, pos):
        self.sprite = Sprite(img, pos)
        self.objects = []
        self.status = init.ALIVE


class Maze:
    """Class to control sprites of mazes, position of objects  and Guardian """
    def __init__(self, maze, assets):
        index = maze.index('G')
        self.guardian = Sprite(assets['guardian'],
                               (index % 15, index // 15))

        self.map = {}
        for index, val in enumerate(maze):
            pos = (index % 15, index // 15)
            if not val:
                self.map[pos] = Sprite(assets["wall"], pos)
            else:
                self.map[pos] = Sprite(assets["floor"], pos)


if __name__ == "__main__":
    game = Game()
    game.run()
