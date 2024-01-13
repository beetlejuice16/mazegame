import os
import sys
import time
import argparse

import pygame
from rich import print, markdown, console

from .builder import create_maze

SIDE_LENGTH = 40

clock = pygame.time.Clock()
walls = []  # List to hold the walls
path = []

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

parser = argparse.ArgumentParser(description="Set dimensions of the maze")
parser.add_argument("Dimension", nargs="?", type=int, choices=range(
    1, 10), default=4, help="An integer to determine the dimensions of the maze")
args = parser.parse_args()
console = console.Console()


# Class for the orange dude
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(32, 32, SIDE_LENGTH, SIDE_LENGTH)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            if self.move_single_axis(dx, 0) == -1:
                return -1
        if dy != 0:
            if self.move_single_axis(0, dy) == -1:
                return -1

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                return -1

    def set_start_position(self, x, y):
        self.rect = pygame.Rect(x, y, SIDE_LENGTH, SIDE_LENGTH)


# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], SIDE_LENGTH, SIDE_LENGTH)


class Path(object):
    def __init__(self, pos):
        path.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], SIDE_LENGTH, SIDE_LENGTH)


level = create_maze(args.Dimension)


# Set up the display
pygame.display.set_caption("Get to the red square!")

screen = pygame.display.set_mode(
    (SIDE_LENGTH * len(level[0]), SIDE_LENGTH * len(level))
)


# Parse the level array above
x = y = 0
for row in level:
    for col in row:
        if col == 1:
            Wall((x, y))
        if col == 0:
            Path((x, y))
        x += SIDE_LENGTH
    y += SIDE_LENGTH
    x = 0


# Draw the scene


end_rect = pygame.Rect(SIDE_LENGTH * (len(level) - 1),
                       (len(level[0]) - 2) * SIDE_LENGTH, SIDE_LENGTH, SIDE_LENGTH)

player = Player()  # Create the player
player.set_start_position(0, SIDE_LENGTH)


def draw_game():
    screen.fill((0, 0, 0))
    for p in path:
        pygame.draw.rect(screen, (205, 133, 63), p.rect, 1)
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect, 5)
        if player.rect.colliderect(wall):
            return -1

    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    # pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.draw.rect(screen, (30, 144, 255), player.rect)
    pygame.display.flip()


def move_player():
    pygame.draw.rect(screen, (30, 144, 255), player.rect)
    pygame.display.flip()


def main():
    running = True
    command_sequence = []
    command_dict = {
        "Down \u2B07": (0, SIDE_LENGTH),
        "Up \u2B06": (0, -SIDE_LENGTH),
        "Left \u2B05": (-SIDE_LENGTH, 0),
        "Right \u2B95": (SIDE_LENGTH, 0),
    }
    draw_game()
    while running:
        clock.tick(60)
        screen.fill((0, 0, 0), player.rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    command_sequence.append("Down \u2B07")
                    print(command_sequence)
                    # player.move(0, SIDE_LENGTH)
                if event.key == pygame.K_UP:
                    command_sequence.append("Up \u2B06")
                    print(command_sequence)
                    # player.move(0, -SIDE_LENGTH)
                if event.key == pygame.K_LEFT:
                    command_sequence.append("Left \u2B05")
                    print(command_sequence)
                    # player.move(-SIDE_LENGTH, 0)
                if event.key == pygame.K_RIGHT:
                    command_sequence.append("Right \u2B95")
                    print(command_sequence)
                    # player.move(SIDE_LENGTH, 0)
                if event.key == pygame.K_RETURN:
                    print("Starting direction sequence.")
                    print(
                        "If you do not reach the end goal you can start a new direction sequence."
                    )
                    for idx, command in enumerate(command_sequence):
                        pygame.time.delay(200)
                        draw_game()
                        # move_player()
                        if player.move(*command_dict[command]) == -1:
                            md = markdown.Markdown("# You have collided.")
                            console.print(md, style="black on yellow")
                            md = markdown.Markdown(
                                "## Your last correct sequence was:")
                            console.print(md, style="green underline")
                            md = markdown.Markdown(
                                f"### {command_sequence[:idx]}")
                            console.print(md)
                            break
                        pygame.time.delay(600)
                    command_sequence = []

        # Just added this to make it slightly fun ;)
        draw_game()
        # move_player()
        if player.rect.colliderect(end_rect):
            md = markdown.Markdown(
                "# You've completed the maze. Well done!")
            console.print(md, style="yellow on black")
            md = markdown.Markdown("# BRAVO LOZO!")
            console.print(md, style="yellow on black")
            time.sleep(1)
            pygame.quit()
            sys.exit()

        clock.tick(360)

    pygame.quit()


if __name__ == "__main__":
    main()
