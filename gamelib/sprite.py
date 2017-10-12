"""
sprite.py - contains sprite classes derived from the pygame.sprite.Sprite class.
"""
import pygame
import gamelib.palette as p


class BaseSprite(pygame.sprite.Sprite):
    """
    Represents the base sprite that moves laterally.
    """
    def __init__(self, color: pygame.Color, width: int, height: int):
        """
        Creates a new BaseSprite instance.

        Args:
            color: a 3 value tuple that represents the BaseSprite's RGB color.
            width: the width of the BaseSprite.
            height: the height of the BaseSprite.
        """
        super().__init__()

        # Create the BaseSprite's surface.
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        # Save the dimensions to the rect attribute.
        self.rect = self.image.get_rect()

        # BaseSprite velocity.
        self.x_speed = 0


    def set_position(self, x: int, y: int):
        """
        Sets the BaseSprite's position on the screen.

        Args:
            x: the x-coordinate.
            y: the y-coordinate.
        """
        self.rect.x, self.rect.y = x, y


    def move_laterally(self, x_speed: int):
        """
        Sets the BaseSprite's x_speed.

        Args:
            x_speed: the new velocity in which the BaseSprite moves on
                the x-axis.
        """
        self.x_speed = x_speed


    def update(self):
        """
        General purpose update method that gets ran when a containing
        pygame.sprite.Group run its own update method.
        """
        # Move the BaseSprite on the x-axis.
        self.rect.x += self.x_speed


class Player(BaseSprite):
    """
    Represents the player-controlled sprite.
    """
    pass


class Zombie(BaseSprite):
    """
    Represents the zombie sprite that tries to overwhelm the player.
    """
    pass