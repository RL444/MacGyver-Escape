""" Module Cell class, inherit from pygame Sprite
and add some module used during this game"""
import pygame

import constant


class Cell(pygame.sprite.Sprite):
    """Enhanced Sprite with functions to ease computation"""

    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            pos[0] * constant.SPRITE_W,
            pos[1] * constant.SPRITE_H,
        )
        self.image.set_colorkey(constant.BLACK)

    @property
    def pos(self):
        """Return tuple position of sprite after conversion from pixel
        to index referential"""
        return (
            self.rect.topleft[0] // constant.SPRITE_W,
            self.rect.topleft[1] // constant.SPRITE_H,
        )

    @pos.setter
    def pos(self, pos):
        """Set position of sprite in pixel from index tuple"""
        self.rect.topleft = (
            pos[0] * constant.SPRITE_W,
            pos[1] * constant.SPRITE_H,
        )

    @property
    def pos_pixel(self):
        """Return position in pixel"""
        return self.rect.topleft

    @pos_pixel.setter
    def pos_pixel(self, pos):
        """Set position of sprite in pixel"""
        self.rect.topleft = (pos[0], pos[1])
