"""
game.py - contains game instance classes.
"""
import pygame
import gamelib.palette as p
from gamelib.sprite import Player


class Game(object):
    """
    Represents the framework for a Pygame project.
    """
    def __init__(self, screen: pygame.Surface, color: tuple, title: str):
        self.screen = screen
        self.color = color
        self.title = title

        # Sprite groups.
        self.all_sprites = pygame.sprite.Group()

        # Create the main player.
        self.player = Player(p.white, 40, 50)
        self.player.set_position(
            screen.get_width() / 2 - self.player.image.get_width() / 2,
            screen.get_height() - 75
        )

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