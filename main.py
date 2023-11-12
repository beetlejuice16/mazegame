import os
import sys
import random
import time
import pygame

SIDE_LENGTH = 32


# Class for the orange dude
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(32, 32, SIDE_LENGTH, SIDE_LENGTH)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

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


# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W  S               W",
    "WWW   W   WWWWWWW  W",
    "WWW   WE           W",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")

screen = pygame.display.set_mode(
    (SIDE_LENGTH * len(level[0]), SIDE_LENGTH * len(level))
)

clock = pygame.time.Clock()
walls = []  # List to hold the walls
path = []
player = Player()  # Create the player


# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == " ":
            Path((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, SIDE_LENGTH, SIDE_LENGTH)
        if col == "S":
            player.set_start_position(x, y)
        x += SIDE_LENGTH
    y += SIDE_LENGTH
    x = 0


# Draw the scene
def draw_game():
    screen.fill((0, 0, 0))
    for p in path:
        pygame.draw.rect(screen, (205, 133, 63), p.rect, 1)
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect, 5)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
    pygame.display.flip()


running = True
command_sequence = []
command_dict = {
    "Down \u2B07": (0, SIDE_LENGTH),
    "Up \u2B06": (0, -SIDE_LENGTH),
    "Left \u2B05": (-SIDE_LENGTH, 0),
    "Right \u27A1": (SIDE_LENGTH, 0),
}
while running:
    clock.tick(60)

    screen.fill((0, 0, 0), player.rect)
    for event in pygame.event.get():
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
                command_sequence.append("Right \u27A1")
                print(command_sequence)
                # player.move(SIDE_LENGTH, 0)
            if event.key == pygame.K_RETURN:
                print("Starting command sequence.")
                print(
                    "If you do not reach the end goal you can start a new command sequence."
                )
                for command in command_sequence:
                    pygame.time.delay(500)
                    player.move(*command_dict[command])
                    draw_game()
                    pygame.time.delay(500)
                command_sequence = []
            if event.key == pygame.K_ESCAPE:
                running = False

    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        print("Well done!")
        time.sleep(1)
        pygame.quit()
        sys.exit()

    draw_game()

    clock.tick(360)

pygame.quit()
