"""
sprite.py - contains sprite classes derived from the pygame.sprite.Sprite class.
"""
import pygame
import gamelib.palette as p

class Block(pygame.sprite.Sprite):
    """
    A simple implementation of a custom sprite class.
    """
    def __init__(self, color: pygame.Color, width: int, height: int):
        """
        Creates a new Block instance.

        Args:
            color: a 3 value tuple that represents the Block's RGB color.
            width: the width of the Block.
            height: the height of the Block.
        """
        super().__init__()

        # Create the Block's surface.
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        # Save the dimensions to the rect attribute.
        self.rect = self.image.get_rect()
