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

SPRITE_H = 40
SPRITE_W = 40
OPTIONAL_H = 1
OPTIONAL_W = 0
MAZE_SIZE = 15

DEAD = 0
ALIVE = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (150, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)

ITEMS = ["plastic_tube", "ether", "needle"]
RESSOURCE_FOLDER = Path(".") / "ressources"

BUTTON_W = 3
BUTTON_H = 1

SMALL_FONT = "comicsansms"
SMALL_SIZE = 25
BIG_FONT = "freesansbold.ttf"
BIG_SIZE = 70
