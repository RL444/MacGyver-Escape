import pygame
import time

import constant
from maze import Maze
from display import Button, Message


class Game:
    """ Class managing the state machine and general information of the Game"""

    def __init__(self):
        # Initialize Pygame basics
        pygame.init()
        self.width = (
            constant.MAZE_SIZE + constant.OPTIONAL_W
        ) * constant.SPRITE_W
        self.height = (
            constant.MAZE_SIZE + constant.OPTIONAL_H
        ) * constant.SPRITE_H

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mac Gyver Escape")
        self.clock = pygame.time.Clock()

        self.start_button = Button(
            (constant.MAZE_SIZE // 5, constant.MAZE_SIZE * 2 // 3),
            constant.GREEN,
            constant.BRIGHT_GREEN,
            "Start",
        )

        self.quit_button = Button(
            (constant.MAZE_SIZE * 3 // 5, constant.MAZE_SIZE * 2 // 3),
            constant.RED,
            constant.BRIGHT_RED,
            "Quit",
        )

        self.menu_message = Message(
            (self.width // 2, self.height // 4),
            "Mac Gyver Escape",
            constant.BIG_SIZE,
            constant.BIG_FONT,
            constant.BLACK
        )

        self.status = constant.MENU

        try:
            self.maze = Maze()
        except RuntimeError:
            print("Error during initialization of Game")
            self.status = constant.EXIT
            return

    def run(self):
        """function used to mange the game display and behavior"""
        while self.status:
            # Keep loop running at the right speed
            self.clock.tick(constant.FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check exit condition
                if event.type == pygame.QUIT:
                    self.status = constant.EXIT

            if self.status == constant.MENU:
                self.screen.fill(constant.WHITE)
                if self.start_button.display(self.screen):
                    self.status = constant.PLAY
                if self.quit_button.display(self.screen):
                    self.status = constant.EXIT
                self.menu_message.display(self.screen)
                pygame.display.flip()

            elif self.status == constant.PLAY:
                self.status = self.maze.update()

                self.screen.fill(constant.BLACK)
                self.maze.display(self.screen)
                pygame.display.flip()

            elif self.status == constant.FINISH:
                self.screen.fill(constant.WHITE)
                result = self.maze.final_result()
                end_message = Message(
                    (self.width // 2, self.height // 2),
                    result,
                    constant.BIG_SIZE,
                    constant.BIG_FONT,
                    constant.BLACK
                )
                end_message.display(self.screen)
                pygame.display.flip()
                time.sleep(1)
                self.status = constant.RESTART

            elif self.status == constant.RESTART:
                self.maze.restart()
                self.status = constant.MENU

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
