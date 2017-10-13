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


class Bullet(BaseSprite):
    """
    Represents the bullet that the Player fires to try and fend off
    the hordes of zombies.
    """
    pass


class Player(BaseSprite):
    """
    Represents the player-controlled sprite.
    """
    def __init__(self, color: pygame.Color, width: int, height: int, bullet_x_speed: int):
        """
        Creates a new Player instance. See the BaseSprite class constructor
        for more information.
        
        Args:
            bullet_x_speed: the speed in which the player's bullets travel at
                the x-axis.
        """
        super().__init__(color, width, height)

        # Bullets from the player.
        self.bullets = pygame.sprite.Group()

        # Set an initial bullet velocity.
        self.bullet_x_speed = abs(bullet_x_speed)


    def calc_bullet_info(self, bullet: Bullet) -> list:
        """
        Calcuates the position and velocity of the player's bullet.
        Returns -> [x, y, x_speed]
            x: x-coordinate of the bullet
            y: y-coordinate of the bullet
            x_speed: velocity of the bullet on the x-axis
        """
        x = None
        # Place the bullet at the right of the player if
        # the player is moving right.
        if self.bullet_x_speed > 0:
            x = self.rect.right + 10  # Some padding.
        
        # And vice-versa if the player is moving left.
        elif self.bullet_x_speed < 0:
            x = self.rect.left - 10   # Some padding.

        # The bullet is half the player's height.
        y = self.rect.center[1] - bullet.image.get_height() / 2

        return [x, y, self.bullet_x_speed]


    def update(self):
        """
        Modified update method to update the bullet's velocity to
        reflect where the player last moved.
        """
        super().update()

        if self.x_speed > 0:
            self.bullet_x_speed = abs(self.bullet_x_speed)
        elif self.x_speed < 0:
            self.bullet_x_speed = -abs(self.bullet_x_speed)


class Zombie(BaseSprite):
    """
    Represents the zombie sprite that tries to overwhelm the player.
    """
    pass
