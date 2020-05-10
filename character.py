""" Contain Player class to manage player action
and status and Guardian class """
from math import copysign

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
        # Boolean to indicate if moving animation is in progress
        self.moving = False
        # Attribut for animation
        self.speed = (0, 0)
        self.target = pos

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

    def set_target(self, target):
        """ Update player target if not in moving animation """
        if not self.moving:
            self.target = target
            self.moving = True

            diff = (self.target[0] - self.pos[0], self.target[1] - self.pos[1])
            # Set speed to constant.SPEED with correct direction
            # or set speed to 0 if target and pos are equal
            self.speed = (
                diff[0] and copysign(constant.SPEED, diff[0]),
                diff[1] and copysign(constant.SPEED, diff[1]),
            )

    def update(self):
        """ Animated player if in moving state,
        do nothing if not moving """

        if self.moving:
            # If player is close to target position set pos at target
            # to ensure a spot at exact target position
            # (if speed is not a modulo of sprite size)
            if self._closed:
                self.pos = self.target
                self.moving = False
            else:
                self.pos_pixel = (
                    self.pos_pixel[0] + self.speed[0],
                    self.pos_pixel[1] + self.speed[1],
                )

    def _to_pixel(self, pos):
        """ Convert position in index into position in pixel """
        return (
            pos[0] * constant.SPRITE_W,
            pos[1] * constant.SPRITE_H,
        )

    @property
    def _closed(self):
        """ player is say closed to target if the distance in pixel between player
        and target is smaller than the speed of player """
        target = self._to_pixel(self.target)
        if (
            abs(self.pos_pixel[0] - target[0]) <= constant.SPEED
            and abs(self.pos_pixel[1] - target[1]) <= constant.SPEED
        ):
            return True
        return False
