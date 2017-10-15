"""
sprite.py - contains sprite classes derived from the pygame.sprite.Sprite class.
"""
import pygame
import rzd.gamelib.palette as p


class BaseSprite(pygame.sprite.Sprite):
    """
    Represents the base sprite that moves in both x and y axis.
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
        self.y_speed = 0


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

    
    def move_vertically(self, y_speed: int):
        """
        Sets the BaseSprite's y_speed.

        Args:
            y_speed: the new velocity in which the BaseSprite moves on
                the y-axis.
        """
        self.y_speed = y_speed


    def update(self):
        """
        General purpose update method that gets ran when a containing
        pygame.sprite.Group run its own update method.
        """
        # Move the BaseSprite on the x-axis.
        self.rect.x += self.x_speed

        # Move the BaseSprite on the y-axis.
        self.rect.y += self.y_speed


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

        # Player stats.
        self.hp = 5
        self.ammo = 10

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
    spawn_interval = 7000       # Zombies spawn every 7 seconds
    interval_difference = 250   # Each spawn gets faster at 1/4 of a second
    current_tick = None         # Replaced with the current clock tick.


class PowerUp(BaseSprite):
    """
    Represents a falling object that gives the player resources.
    """
    spawn_interval = 5000           # Powerup spawns every 5 seconds
    interval_difference = -100      # Each spawn gets slower at 1/10 of a second
    current_tick = None             # Replaced with the current clock tick.

    def __init__(self, color: pygame.Color, width: int, height: int, screen: pygame.Surface):
        """
        Creates a new PowerUp instance. See BaseSprite class for inherited paremeters.
        
        Args:
            screen: the surface in which the PowerUp is to be drawn.
        """
        super().__init__(color, width, height)

        self.screen = screen


    def update(self):
        """
        Modified update method to prevent the PowerUp from dropping
        off screen.
        """
        super().update()

        # Check if at the bottom of the screen.
        if self.rect.bottom >= self.screen.get_height() - 25:
            self.rect.bottom = self.screen.get_height() - 25


class HealthPack(PowerUp):
    """
    Represents a powerup that gives the player some health points
    when picked up.
    """
    def __init__(self, color: pygame.Color, width: int, height: int, screen: pygame.Surface, heal_amount: int):
        """
        Creates a new HealthPack instance. See PowerUp class for inherited paremeters.
        
        Args:
            heal_amount: the amount of health that the player replenishes when
                this pack is picked up.
        """
        super().__init__(color, width, height, screen)

        self.heal_amount = heal_amount


    def __repr__(self):
        return "<HealthPack +{} />".format(self.heal_amount)


class AmmoPack(PowerUp):
    """
    Represents a powerup that gives the player some ammunition
    when picked up.
    """
    def __init__(self, color: pygame.Color, width: int, height: int, screen: pygame.Surface, ammo_count: int):
        """
        Creates a new AmmoPack instance. See PowerUp class for inherited paremeters.
        
        Args:
            ammo_count: the amount of ammo that the player replenishes when
                this pack is picked up.
        """
        super().__init__(color, width, height, screen)

        self.ammo_count = ammo_count


    def __repr__(self):
        return "<AmmoPack +{} />".format(self.ammo_count)
