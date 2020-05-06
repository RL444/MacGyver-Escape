""" Contain Player class to manage player action and status and Guardian class """

import constant

from cell import Cell


class Player(Cell):
    """ Manage player movement and status """

    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.items = []
        self.status = constant.ALIVE
        self._initial_pos = pos

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
        if len(self.items) >= len(constant.ITEMS):
            return True
        return False

    def add_item(self, item):
        index = len(self.items)
        item.pos = (index, constant.MAZE_SIZE)
        self.items.append(item)

    def death(self):
        self.status = constant.DEAD

    def restart(self):
        self.pos = self._initial_pos
        self.status = constant.ALIVE
        items = []
        for item in self.items[:]:
            items.append(self.items.pop())
        return items


class Guardian(Cell):
    """ Cell with alive status for end of game """

    def __init__(self, img, pos):
        super().__init__(img, pos)
        self.status = constant.ALIVE
        self._initial_pos = pos

    def death(self):
        self.status = constant.DEAD

    def restart(self):
        self.pos = self._initial_pos
        self.status = constant.ALIVE
