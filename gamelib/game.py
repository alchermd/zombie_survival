"""
game.py - contains game instance classes.
"""
import pygame
import gamelib.palette as p
from gamelib.sprite import Player, Zombie, Bullet


class Game(object):
    """
    Represents the framework for a Pygame project.
    """
    def __init__(self, screen: pygame.Surface, color: tuple, title: str):
        self.screen = screen
        self.color = color
        self.title = title
        self.clock = pygame.time.Clock()

        # Sprite groups.
        self.all_sprites = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()

        # Create the main player.
        self.player = Player(p.white, 40, 50, 25)
        self.player.set_position(
            screen.get_width() / 2 - self.player.image.get_width() / 2,
            screen.get_height() - 75
        )

        # Create 6 zombies, 3 from left and
        # 3 from right, to test issue #2
        for i in range(3):
            zombie = Zombie(p.red, 40, 50)
            zombie.set_position(
                -(40 + i * 60),
                screen.get_height() - 75
            )
            zombie.move_laterally(3)
            zombie.add(self.all_sprites, self.zombies)
        
        for i in range(3):
            zombie = Zombie(p.red, 40, 50)
            zombie.set_position(
                screen.get_width() + 40 + i * 60,
                screen.get_height() - 75
            )
            zombie.move_laterally(-3)
            zombie.add(self.all_sprites, self.zombies)

        # Save sprites.
        self.all_sprites.add(self.player)

    
    def handle_events(self) -> bool:
        """
        Processes the events in the Pygame event queue.

        Returns:
            A boolean value indicating whether the game is still
            processing events or not.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Bind LEFT and RIGHT keys to player movement.
                if event.key == pygame.K_LEFT:
                    self.player.move_laterally(-5)
                if event.key == pygame.K_RIGHT:
                    self.player.move_laterally(5)


                # Bind SPACE to shoot bullets.
                if event.key == pygame.K_SPACE: 
                    if self.player.ammo > 0:
                        # Create a new bullet.
                        bullet = Bullet(p.blue, 20, 20)

                        # Set its position and velocity.
                        bullet_x, bullet_y, bullet_x_speed = self.player.calc_bullet_info(bullet)
                        bullet.set_position(bullet_x, bullet_y)
                        bullet.move_laterally(bullet_x_speed)

                        # Save the bullet.
                        bullet.add(self.all_sprites, self.player.bullets)

                        # Reduce the player's ammo.
                        self.player.ammo -= 1
                        print("Ammo: {:2}".format(self.player.ammo))
                    
                    else:
                        print("No more ammo.")


            if event.type == pygame.KEYUP:
                # Smoothen the player's movement.
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.move_laterally(0)


        return True


    def run_game_logic(self):
        """
        Runs the logic for running the game.
        """
        self.all_sprites.update()

        # Check for bullet to zombie collisions.
        for bullet in self.player.bullets:
            zombies_hit = pygame.sprite.spritecollide(bullet, self.zombies, True)
            if zombies_hit:
                bullet.kill()

        # Check for zombie to player collisions.
        zombies_hit = pygame.sprite.spritecollide(self.player, self.zombies, True)
        for zombie in zombies_hit:
            self.player.hp -= 1
            print("HP: {:2}".format(self.player.hp))

        # Check for win / lose conditions.
        if self.player.hp <= 0:
            print("You lost!")


    def display_frame(self, screen: pygame.Surface=None):
        """
        Updates the Pygame display.

        Args:
            screen: Pygame surface to draw on.
        """
        if screen is None:
            screen = self.screen

        screen.fill(self.color)

        self.all_sprites.draw(screen)

        pygame.display.flip()