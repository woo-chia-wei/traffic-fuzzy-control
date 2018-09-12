import pygame
from src.Common import Lane
from src.Config import Config
from src.VehicleFactory import VehicleFactory

# Configuration
spawn_gap = 1500
frame_rate = 30

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
dark_gray = (169, 169, 169)
dark_yellow = (204, 204, 0)

# Create game
pygame.init()
surface = pygame.display.set_mode((Config['simulator']['screen_width'], Config['simulator']['screen_height']))
pygame.display.set_caption('Fuzzy Car')
clock = pygame.time.Clock()
factory = VehicleFactory(surface)


def main_loop():

    game_over = False

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, spawn_gap)

    while not game_over:

        for event in pygame.event.get():

            if event.type == SPAWN_EVENT:
                factory.create_vehicle(Lane.right_to_left)
                factory.create_vehicle(Lane.left_to_right)
                factory.create_vehicle(Lane.top_to_bottom)
                factory.create_vehicle(Lane.bottom_to_top)

            if event.type == pygame.QUIT:
                game_over = True

        # Refresh background
        surface.fill(white)

        factory.update_and_draw_vehicles()

        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == "__main__":
    main_loop()
    pygame.quit()
    quit()
