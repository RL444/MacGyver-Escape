""" Contain Player class to manage player action and status and Guardian class """

import constant

from cell import Cell


class Character(Cell):
    """ Cell with alive status to define end of game """

    def __init__(self, img, pos):
        """ Cell with management of live status """
        super().__init__(img, pos)
        self.status = constant.ALIVE
        # Save initial pos for restart
        self._initial_pos = pos

    def death(self):
        self.status = constant.DEAD

    def restart(self):
        """ reset essential attribut in case of restart """
        self.pos = self._initial_pos
        self.status = constant.ALIVE


class Player(Character):
    """ Manage player movement and status """

    def __init__(self, img, pos):
        """ character with items stockage """
        super().__init__(img, pos)
        self.items = []

    # property to return the indicate surrounding cell position
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

    # move function for player key arrow displacement
    def move_left(self):
        self.pos = (self.pos[0] - 1, self.pos[1])

    def move_right(self):
        self.pos = (self.pos[0] + 1, self.pos[1])

    def move_up(self):
        self.pos = (self.pos[0], self.pos[1] - 1)

    def move_down(self):
        self.pos = (self.pos[0], self.pos[1] + 1)

    @property
    def ready(self):
        """ If player has enough items he is ready to fight guardian """
        if len(self.items) >= len(constant.ITEMS):
            return True
        return False

    def add_item(self, item):
        """ add a item in the self.items container
        and set is postition to be display under the maze """
        index = len(self.items)
        item.pos = (index, constant.MAZE_SIZE)
        self.items.append(item)

    def restart(self):
        """ reset essential attribut in case of restart
        and return items inside maze"""
        super().restart()
        items = []
        for item in self.items[:]:
            items.append(self.items.pop())
        return items
