import json
from random import randint

import pygame
from pathlib import Path

import init


class Game:
    """ Class managing the state machine and general information of the Game"""

    def __init__(self):
        # Initialize Pygame basics
        pygame.init()
        self.width = (init.MAZE_W + init.OPTIONAL_W) * init.SPRITE_W
        self.height = (init.MAZE_H + init.OPTIONAL_H) * init.SPRITE_H
        self.screen = pygame.display.set_mode((self.width, self.height))
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

        ressources = Path(".") / "ressources"
        try:
            with open(str(ressources / "data.json"), "r") as json_files:
                data = json.load(json_files)
                # Load all sprites inside a list for easy access
                self.assets = self.__load_assets(ressources, data["List of sprites"])
                # Load map of the maze store inside data.json, also contain
                # position for Player and Guardian
                maze = data["maze"]

                # Initialize Maze
                self.maze = Maze(maze, self.assets)

                # Add sprite in sprite_group
                for sprite in self.maze.map.values():
                    self.all_sprites.add(sprite)
                for sprite in self.maze.items:
                    self.all_sprites.add(sprite)
                self.all_sprites.add(self.maze.guardian)
                self.all_sprites.add(self.maze.player.sprite)

        except (FileNotFoundError, FileExistsError) as error:
            print(error)
            print("Please check ressource folder before playing Game")
            self.status = init.EXIT
        except KeyError as error:
            print(f"error while attempting to read {error}" + "from data.jon file")
            self.status = init.EXIT

    def run(self):
        """function used to mange the game display and behavior"""
        while self.status:
            # Keep loop running at the right speed
            self.clock.tick(init.FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.status = init.EXIT

            # Display depending on game status
            if self.status == init.MENU:
                self.display_message("MacGyver Escape")

                self.button(
                    "GO!",
                    self.width * 1 / 5,
                    self.height * 2 / 3,
                    100,
                    50,
                    init.GREEN,
                    init.BRIGHT_GREEN,
                    init.PLAY,
                )
                self.button(
                    "Quit",
                    self.width * 2 / 3,
                    self.height * 2 / 3,
                    100,
                    50,
                    init.RED,
                    init.BRIGHT_RED,
                    init.EXIT,
                )

                pygame.display.update()

            elif self.status == init.PLAY:
                self.screen.fill(init.BLACK)
                # TODO
                self.maze.update(self.assets)
                if (
                    self.maze.player.status == init.DEAD
                    or self.maze.player.status == init.WINNER
                ):
                    self.status = init.FINISH
                self.all_sprites.update()
                self.all_sprites.draw(self.screen)
                pygame.display.flip()

            elif self.status == init.FINISH:
                sentence = f"You are {'DEAD' if self.maze.player.status == init.DEAD else 'WINNER'}"
                self.display_message(sentence)

                self.button(
                    "Restart",
                    self.width * 1 / 5,
                    self.height * 2 / 3,
                    100,
                    50,
                    init.GREEN,
                    init.BRIGHT_GREEN,
                    init.RESTART,
                )
                self.button(
                    "Quit",
                    self.width * 2 / 3,
                    self.height * 2 / 3,
                    100,
                    50,
                    init.RED,
                    init.BRIGHT_RED,
                    init.EXIT,
                )

                pygame.display.update()

            elif self.status == init.RESTART:
                self.__init__()
                self.status = init.PLAY

        pygame.quit()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, init.BLACK)
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))
            if click[0] == 1 and action is not None:
                self.status = action
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurf, textRect)

    def display_message(self, sentence):
        """Display sentence on screen on white fill background"""
        self.screen.fill(init.WHITE)
        largeText = pygame.font.Font("freesansbold.ttf", 60)
        TextSurf, TextRect = self.text_objects(sentence, largeText)
        TextRect.center = ((self.width / 2), (self.height / 3))
        self.screen.blit(TextSurf, TextRect)


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
        return (
            self.rect.topleft[0] // init.SPRITE_W,
            self.rect.topleft[1] // init.SPRITE_H,
        )

    @pos.setter
    def pos(self, pos):
        """Set position of sprite in pixel from index tuple"""
        self.rect.topleft = (pos[0] * init.SPRITE_W, pos[1] * init.SPRITE_H)


class Player:
    """Class to store status of player"""

    def __init__(self, img, pos):
        self.sprite = Sprite(img, pos)
        self.items = []
        self.status = init.ALIVE

    @property
    def pos(self):
        return self.sprite.pos

    @property
    def pos_left(self):
        return (self.pos[0] - 1, self.pos[1])

    @property
    def pos_right(self):
        return (self.pos[0] + 1, self.pos[1])

    @property
    def pos_up(self):
        return (self.pos[0], self.pos[1] - 1)

    @property
    def pos_down(self):
        return (self.pos[0], self.pos[1] + 1)

    @property
    def move_left(self):
        self.sprite.pos = (self.sprite.pos[0] - 1, self.sprite.pos[1])

    @property
    def move_right(self):
        self.sprite.pos = (self.sprite.pos[0] + 1, self.sprite.pos[1])

    @property
    def move_up(self):
        self.sprite.pos = (self.sprite.pos[0], self.sprite.pos[1] - 1)

    @property
    def move_down(self):
        self.sprite.pos = (self.sprite.pos[0], self.sprite.pos[1] + 1)


class Maze:
    """Class to control state of Maze, update sprites postition
    and status of maze"""

    def __init__(self, maze, assets):
        # Initialize Guardian
        index = maze.index("G")
        self.guardian = Sprite(assets["guardian"], (index % 15, index // 15))

        # Initialize player
        index = maze.index("P")
        self.player = Player(assets["player"], (index % 15, index // 15))

        # Initialize all sprite for maze background
        self.map = {}
        for index, val in enumerate(maze):
            pos = (index % 15, index // 15)
            if not val:
                self.map[pos] = Sprite(assets["wall"], pos)
            else:
                self.map[pos] = Sprite(assets["floor"], pos)

        # Initialize items in random position
        self.items = []
        sprites_items = ["plastic_tube", "ether", "needle"]
        while len(self.items) < 3:
            pos = (randint(0, 14), randint(0, 14))
            if (
                self.map[pos].image == assets["floor"]
                and self.guardian.pos != pos
                and self.player.pos != pos
            ):
                self.items.append(Sprite(assets[sprites_items[len(self.items)]], pos))

    def update(self, assets):
        """Update the status of the maze each frame"""
        keystate = pygame.key.get_pressed()
        if (
            keystate[pygame.K_LEFT]
            and self.player.pos_left[0] >= 0
            and self.map[self.player.pos_left].image == assets["floor"]
        ):
            self.player.move_left

        if (
            keystate[pygame.K_RIGHT]
            and self.player.pos_right[0] < init.MAZE_W
            and self.map[self.player.pos_right].image == assets["floor"]
        ):
            self.player.move_right

        if (
            keystate[pygame.K_UP]
            and self.player.pos_up[1] >= 0
            and self.map[self.player.pos_up].image == assets["floor"]
        ):
            self.player.move_up

        if (
            keystate[pygame.K_DOWN]
            and self.player.pos_down[1] < init.MAZE_H
            and self.map[self.player.pos_down].image == assets["floor"]
        ):
            self.player.move_down

        if self.player.pos == self.guardian.pos:
            if len(self.player.items) > 2:
                self.player.status = init.WINNER
            else:
                self.player.status = init.DEAD

        for i, sprite in enumerate(self.items[:]):
            if sprite.pos == self.player.pos:
                self.player.items.append(self.items.pop(i))
                index = len(self.player.items) - 1
                self.player.items[index].pos = (index, init.MAZE_H + 1)


if __name__ == "__main__":
    game = Game()
    game.run()
