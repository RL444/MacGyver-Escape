from pathlib import Path

# Status for game state
# Exit kill pygame screen and exit application
EXIT = 0
# Display starting Menu
MENU = 1
# Display end of game result
FINISH = 2
# Game is playing now
PLAY = 3
# Game in pause and display instructions for player
PAUSE = 4
# Game initialize again game for a new try
RESTART = 5

FPS = 10

# Dimension of maze and sprites
MAZE_SIZE = 15
SPRITE_H = 40
SPRITE_W = 40
# optional space in height of width direction
# to add comment or information on the game
# for example
OPTIONAL_H = 1
OPTIONAL_W = 0

# Life status for player and Guardian
DEAD = 0
ALIVE = 1
# Speed (pixel per clock loop) of player during displacements
SPEED = 10

# Colors for screen display
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)

# Ressource folder
RESSOURCE_FOLDER = Path(".") / "ressources"
# image used as objects during game
ITEMS = ["plastic_tube", "ether", "needle"]
WEAPON = "syringe"

# Information on buttons and message during game
BUTTON_W = 3
BUTTON_H = 1
SMALL_FONT = "comicsansms"
SMALL_SIZE = 25
BIG_FONT = "freesansbold.ttf"
BIG_SIZE = 70
