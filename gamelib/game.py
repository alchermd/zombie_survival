"""
game.py - contains game instance classes.
"""
import pygame
import random
import gamelib.palette as p
from gamelib.sprite import Player, Zombie, Bullet, PowerUp, HealthPack, AmmoPack


class Game(object):
    """
    Represents the framework for a Pygame project.
    """
    def __init__(self, screen: pygame.Surface, color: tuple, title: str):
        # Display attributes.
        self.screen = screen
        self.color = color
        self.title = title

        # Clock and time.
        self.clock = pygame.time.Clock()
        Zombie.last_tick = pygame.time.get_ticks()
        PowerUp.last_tick = pygame.time.get_ticks()

        # Toggled for early game exits.
        self.aborted = False

        # Sprite groups.
        self.all_sprites = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Create the main player.
        self.player = Player(p.white, 40, 50, 25)
        self.player.set_position(
            screen.get_width() / 2 - self.player.image.get_width() / 2,
            screen.get_height() - 75
        )

        # Save sprites.
        self.all_sprites.add(self.player)
    

    def create_powerups(self, n: int):
        """
        Create new powerups that will get spawned on the
        next update() call.

        Args:
            n: the amount of powerups that spawn. Half of n will
             HealthPacks and half will be AmmoPacks
        """
        for i in range(n):
            if i % 2 == 0:
                # Create a new health pack.        
                healthpack = HealthPack(p.green, 20, 20, self.screen, 5)

                # Randomly set its position.
                healthpack.set_position(
                    random.randrange(self.screen.get_width() - 20),
                    random.randrange(-100, 0)
                )

                # Set its vertical speed.
                healthpack.move_vertically(2)

                # Save sprite.
                healthpack.add(self.powerups, self.all_sprites)

            else:
                # Create a new health pack.   
                ammopack = AmmoPack(p.white, 20, 20, self.screen, 5) 

                # Randomly set its position.
                ammopack.set_position(
                    random.randrange(self.screen.get_width() - 20),
                    random.randrange(-100, 0)
                )

                # Set its vertical speed.
                ammopack.move_vertically(2)

                # Save sprite.
                ammopack.add(self.powerups, self.all_sprites)


    def create_zombies(self, n: int, right: int=None):
        """
        Create new zombies that will get spawned on the
        next update() call.

        Args:
            n: the amount of zombies that spawn on each side.
            right: if given, n will constitute to the zombies
                to the left.
        """
        if right is None:
            right = n
        
        # Zombies from the left.
        for i in range(n):
            zombie = Zombie(p.red, 40, 50)
            zombie.set_position(
                -(40 + i * 60),
                self.screen.get_height() - 75
            )
            zombie.move_laterally(3)
            zombie.add(self.all_sprites, self.zombies)
        
        # Zombies from the right.
        for i in range(right):
            zombie = Zombie(p.red, 40, 50)
            zombie.set_position(
                self.screen.get_width() + 40 + i * 60,
                self.screen.get_height() - 75
            )
            zombie.move_laterally(-3)
            zombie.add(self.all_sprites, self.zombies)


    def handle_events(self) -> bool:
        """
        Processes the events in the Pygame event queue.

        Returns:
            A boolean value indicating whether the game is still
            processing events or not.
        """
        # Check for early game exits.
        if self.aborted:
            return False

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

        # Check if enough time has passed to spawn zombies.
        Zombie.current_tick = pygame.time.get_ticks()
        if Zombie.current_tick - Zombie.last_tick >= Zombie.spawn_interval:
            Zombie.spawn_interval -= Zombie.interval_difference
            Zombie.last_tick = Zombie.current_tick
            self.create_zombies(3)

        # Check if enough time has passed to drop powerups.
        PowerUp.current_tick = pygame.time.get_ticks()
        if PowerUp.current_tick - PowerUp.last_tick >= PowerUp.spawn_interval:
            PowerUp.spawn_interval -= PowerUp.interval_difference
            PowerUp.last_tick = PowerUp.current_tick
            self.create_powerups(2)

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

        # Check for powerup to player collisions.
        powerups_hit = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerups_hit:
            if isinstance(powerup, HealthPack):
                self.player.hp += powerup.heal_amount
                print("HP: {:2}".format(self.player.hp))
            elif isinstance(powerup, AmmoPack):
                self.player.ammo += powerup.ammo_count
                print("Ammo: {:2}".format(self.player.ammo))

        
        # Check for win / lose conditions.
        if self.player.hp <= 0:
            self.abort_game("You lost!")


    def abort_game(self, message: str):
        """
        Preemptively aborts the game.

        Args:
            message: an exit message to be printed to the console.
        """
        self.aborted = True
        print(message)


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