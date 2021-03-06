""" Contain Class Maze that manage maze and its components """
import json
from random import randint

import pygame

import constant
from cell import Cell
from character import Character, Player
from display import Message


class Maze:
    """ Class that contain maze, player, guardian and items
    and control update of game components """

    def __init__(self):
        # Load info from .json file
        data = self._load_data()

        if data is None:
            raise RuntimeError

        # Load image of the game
        self.assets = self._load_assets(data["List of sprites"])
        if self.assets is None:
            raise RuntimeError

        maze = data["Maze"]
        # Initialize all sprite for maze background
        self.map = {}
        for index, val in enumerate(maze):
            pos = (index % constant.MAZE_SIZE, index // constant.MAZE_SIZE)
            if not val:
                self.map[pos] = Cell(self.assets["wall"], pos)
            else:
                self.map[pos] = Cell(self.assets["floor"], pos)

        # Initialize Guardian
        index = maze.index("G")
        self.guardian = Character(
            self.assets["guardian"],
            (index % constant.MAZE_SIZE, index // constant.MAZE_SIZE),
        )

        # Initialize player
        index = maze.index("P")
        self.player = Player(
            self.assets["player"],
            (index % constant.MAZE_SIZE, index // constant.MAZE_SIZE),
        )

        # Initialize items in random position
        self.items = []
        for i in range(3):
            self.items.append(
                Cell(self.assets[constant.ITEMS[i]], self._random_pos())
            )

        # Sprite group for display
        self.all_sprites = pygame.sprite.Group()

        for sprite in self.map.values():
            self.all_sprites.add(sprite)
        for sprite in self.items:
            self.all_sprites.add(sprite)
        self.all_sprites.add(self.guardian)
        self.all_sprites.add(self.player)

        # Create Message and Cell to display
        # if player collect enough items to fight guardian

        self.not_ready_message = Message(
            (
                constant.MAZE_SIZE * constant.SPRITE_W * 3 // 4,
                constant.MAZE_SIZE * constant.SPRITE_H
                + constant.SPRITE_H // 2,
            ),
            "Mac Gywer not Ready, Be Carefull",
            constant.SMALL_SIZE,
            constant.BIG_FONT,
            constant.RED,
        )

        self.ready_message = Message(
            (
                constant.MAZE_SIZE * constant.SPRITE_W * 4 // 5,
                constant.MAZE_SIZE * constant.SPRITE_H
                + constant.SPRITE_H // 2,
            ),
            "Ready to Fight",
            constant.SMALL_SIZE,
            constant.BIG_FONT,
            constant.GREEN,
        )

        self.arrow = Cell(
            self.assets[constant.ARROW_NAME],
            (len(constant.ITEMS) + 1, constant.MAZE_SIZE),
        )
        self.weapon = Cell(
            self.assets[constant.WEAPON],
            (
                len(constant.ITEMS) + constant.ARROW_SIZE + 1,
                constant.MAZE_SIZE,
            ),
        )
        self.weapon_sprites = pygame.sprite.Group()
        self.weapon_sprites.add(self.arrow)
        self.weapon_sprites.add(self.weapon)

    def restart(self):
        returned_items = self.player.restart()
        for item in returned_items:
            self.items.append(item)
        for item in self.items:
            item.pos = self._random_pos()
        self.guardian.restart()

    def _random_pos(self):
        """ Function that return a valid random position
        for a game items """
        valid_pos = False
        # TODO
        while not valid_pos:
            pos = (
                randint(0, constant.MAZE_SIZE - 1),
                randint(0, constant.MAZE_SIZE - 1),
            )
            if (
                self.map[pos].image == self.assets["floor"]
                and pos != self.guardian.pos
                and pos != self.player.pos
            ):
                valid_pos = pos

            # Avoid to have 2 objects at same position
            for item in self.items:
                if valid_pos == item.pos:
                    valid_pos = False

        return valid_pos

    def _load_data(self):
        """ Load Game information inside data.json file
        and return it """
        data_file = constant.RESSOURCE_FOLDER / "data.json"
        try:
            with open(str(data_file), "r") as json_file:
                data = json.load(json_file)

            return data

        except (FileNotFoundError, FileExistsError) as error:
            print(error)
            print("Please check ressource folder before playing Game")
            return

        except KeyError as error:
            print(
                f"error while attempting to read {error}"
                + "from data.jon file"
            )
            return

    def _load_assets(self, files_names):
        """ Load Images coresponding to name inside files_names parameter
        return a list with all this converted images """
        folder = constant.RESSOURCE_FOLDER
        storage = {}
        try:
            for path in [folder / str(name + ".png") for name in files_names]:
                storage[path.stem] = pygame.image.load(str(path)).convert()
        except RuntimeError as error:
            print(error)
            return

        return storage

    def display(self, screen):
        """ Display all maze sprites """
        self.all_sprites.draw(screen)
        if self.player.ready:
            self.ready_message.display(screen)
            self.weapon_sprites.draw(screen)
        else:
            self.not_ready_message.display(screen)

    def update(self):
        """Update the status of the maze each clock loop"""
        if self.player.pos == self.guardian.pos:
            if self.player.ready:
                self.guardian.death()
            else:
                self.player.death()
            # If combat between guardian and player: end of the game
            return constant.FINISH

        # player collect an item if on same position
        for i, sprite in enumerate(self.items[:]):
            if sprite.pos == self.player.pos:
                self.player.add_item(self.items.pop(i))

        # Check key pressed for movements
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            target = self.player.pos_left
        elif keystate[pygame.K_RIGHT]:
            target = self.player.pos_right

        elif keystate[pygame.K_UP]:
            target = self.player.pos_up

        elif keystate[pygame.K_DOWN]:
            target = self.player.pos_down
        else:
            target = None

        if target is not None and self._is_valid(target):
            self.player.set_target(target)

        self.player.update()

        return constant.PLAY

    def _is_valid(self, pos):
        """ return is pos cell can be walk in by player """
        if (
            pos[0] >= 0
            and pos[1] >= 0
            and pos[0] < constant.MAZE_SIZE
            and pos[1] < constant.MAZE_SIZE
            and self.map[pos].image == self.assets["floor"]
        ):
            return True
        return False

    def final_result(self):
        """ Return a string to indicate win or lose
        depending on player and guardian status """
        if self.player.status:
            return "You deliver Mac Gyver !!"
        return "You lose, try again!!"
