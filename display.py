""" Module for class to display informative object on screen """

import pygame

import constant


class Button:
    """ Interactive button link with different color for hover
    and return if it had been clicked during display """

    def __init__(self, pos, color, color_hover, message):
        """ Initialize a rect object, colors and
        a Message instance display in rect center """
        self.rect = pygame.Rect(
            pos[0] * constant.SPRITE_W,
            pos[1] * constant.SPRITE_H,
            constant.BUTTON_W * constant.SPRITE_W,
            constant.BUTTON_H * constant.SPRITE_H,
        )
        self.color = color
        self.color_hover = color_hover
        self.message = Message(
            self.rect.center,
            message,
            constant.SMALL_SIZE,
            constant.BIG_FONT,
            constant.BLACK,
        )

    def _contain(self, pos):
        """ return is Button instance contain the position pos """
        if (
            self.width_min <= pos[0]
            and self.width_max >= pos[0]
            and self.height_min <= pos[1]
            and self.height_max >= pos[1]
        ):
            return True
        return False

    def display(self, screen):
        """ Display button depending on mouse position
        if clicked, return True, False otherwise """
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.color_hover, self.rect)
            self.message.display(screen)
            if clicked[0]:
                return True
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            self.message.display(screen)
        return False


class Message:
    """ Set a message to be displayed with 2 possible size: Big and Small """

    def __init__(self, pos, text, size, font, color):
        self.font = pygame.font.SysFont(font, size)
        self.textSurface = self.font.render(text, True, color)
        self.rect = self.textSurface.get_rect()
        self.rect.center = pos

    def display(self, screen):
        screen.blit(self.textSurface, self.rect)
