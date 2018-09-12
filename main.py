import pygame
import glob
import random
from src.Vehicle import Vehicle
from src.Common import Lane

# Configuration
screen_width = 800
screen_height = 800
spawn_gap = 1500
vehicle_speed = 3
vehicle_width = 40
vehicle_height = 70
frame_rate = 30
safe_distance = 30
vehicle_divider_distance = 10
divider_width = 5

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
dark_gray = (169, 169, 169)
dark_yellow = (204, 204, 0)

# Icons
vehicle_icons = [pygame.image.load(f) for f in glob.glob('images/vehicles_l2r/*.png')]

# Create game
pygame.init()
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fuzzy Car')
clock = pygame.time.Clock()


def random_vehicle_icon():
    return random.choice(vehicle_icons)


v1 = Vehicle(200, 200, Lane.left_to_right, random_vehicle_icon(), surface)
v2 = Vehicle(300, 300, Lane.top_to_bottom, random_vehicle_icon(), surface)

def main_loop():

    game_over = False

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

        # Refresh background
        surface.fill(white)

        v1.move()
        v1.draw()

        v2.move()
        v2.draw()

        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == "__main__":
    main_loop()
    pygame.quit()
    quit()
