import argparse
import pygame

from core.Game import Game

def argument_parse():
    parser = argparse.ArgumentParser(
        prog = 'Snake Game',
        description = 'Snake game being developed with python. ')

    return parser.parse_args()

if __name__ == "__main__":
    args = argument_parse()
    pygame.init()

    game_engine = Game()

    clock = pygame.time.Clock()

    while game_engine.is_running():
        game_engine.update()
        game_engine.render()

    pygame.quit()