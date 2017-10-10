"""
game.py - contains game instance classes.
"""
import pygame
import gamelib.palette as p

class Game(object):
    """
    Represents the framework for a Pygame project.
    """
    def __init__(self, screen: pygame.Surface, color: tuple, title: str):
        self.screen = screen
        self.color = color
        self.title = title

    
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

        return True


    def run_game_logic(self):
        """
        Runs the logic for running the game.
        """
        pass


    def display_frame(self, screen: pygame.Surface=None):
        """
        Updates the Pygame display.

        Args:
            screen: Pygame surface to draw on.
        """
        if screen is None:
            screen = self.screen

        screen.fill(self.color)

        pygame.display.flip()