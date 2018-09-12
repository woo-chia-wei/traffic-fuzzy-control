import pygame
import glob
import random

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


# Decorate environments
def draw_environments():
    # Draw dividers
    x = 0

    y = screen_height / 2 - (vehicle_width + 2 * vehicle_divider_distance) - divider_width / 2
    pygame.draw.rect(surface, dark_gray, (x, y, screen_width, divider_width))

    y = screen_height / 2 - divider_width / 2
    pygame.draw.rect(surface, dark_gray, (x, y, screen_width, divider_width))

    y = screen_height / 2 + (vehicle_width + 2 * vehicle_divider_distance) - divider_width / 2
    pygame.draw.rect(surface, dark_gray, (x, y, screen_width, divider_width))

    # Draw yellow bars
    for n in range(10):
        pygame.draw.rect(surface, dark_yellow, (screen_width / 20 + n * screen_width / 10,
                                                screen_height / 2 - (vehicle_width + vehicle_divider_distance) / 2 - 2,
                                                screen_width / 20, 2))
        pygame.draw.rect(surface, dark_yellow, (screen_width / 20 + n * screen_width / 10,
                                                screen_height / 2 + (vehicle_width + vehicle_divider_distance) / 2 + 2,
                                                screen_width / 20, 2))

class Vehicle:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))


def quit_game():
    pygame.quit()
    quit()


def random_vehicle_icon():
    return random.choice(vehicle_icons)


def spawn_vehicle_l2r(vehicles):
    x = 0
    y = screen_height / 2 - vehicle_width - vehicle_divider_distance
    vehicle = Vehicle(x, y, random_vehicle_icon())
    vehicles.append(vehicle)
    return vehicle


def spawn_vehicle_r2l(vehicles):
    x = screen_width
    y = screen_height / 2 + vehicle_divider_distance
    vehicle = Vehicle(x, y, random_vehicle_icon())
    vehicles.append(vehicle)
    return vehicle


def main_loop():
    vehicles_l2r = []
    vehicles_r2l = []
    game_over = False

    # Set events
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, spawn_gap)

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == SPAWN_EVENT:
                spawn_vehicle_l2r(vehicles_l2r)
                spawn_vehicle_r2l(vehicles_r2l)

        # Refresh background
        surface.fill(white)

        # Draw streets (environments)
        draw_environments()

        # Left to Right Lane
        for index, vehicle in enumerate(vehicles_l2r):
            vehicle.x += vehicle_speed
            vehicle.draw(surface)

        # Right to Left Lane
        for index, vehicle in enumerate(vehicles_r2l):
            vehicle.x -= vehicle_speed
            vehicle.draw(surface)

        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == "__main__":
    main_loop()
    pygame.quit()
    quit()
